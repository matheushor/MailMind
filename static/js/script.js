const form = document.getElementById('emailForm');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const removeFile = document.getElementById('removeFile');
const emailContent = document.getElementById('emailContent');
const submitBtn = document.getElementById('submitBtn');
const submitText = document.getElementById('submitText');
const loadingText = document.getElementById('loadingText');
const results = document.getElementById('results');
const resultContent = document.getElementById('resultContent');
const error = document.getElementById('error');
const errorMessage = document.getElementById('errorMessage');

fileInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        fileName.textContent = file.name;
        fileInfo.classList.remove('hidden');
        
        if (file.type === 'text/plain') {
            const reader = new FileReader();
            reader.onload = function(e) {
                emailContent.value = e.target.result;
            };
            reader.readAsText(file);
        }
    }
});


removeFile.addEventListener('click', function() {
    fileInput.value = '';
    fileInfo.classList.add('hidden');
    emailContent.value = '';
});


form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(form);
    
   
    submitBtn.disabled = true;
    submitText.style.display = 'none';
    loadingText.classList.add('active');
    results.classList.add('hidden');
    error.classList.add('hidden');
    
    try {
        const response = await fetch('/classify', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Erro na classificação');
        }
        
        displayResults(data);
        
    } catch (err) {
        console.error('Error:', err);
        errorMessage.textContent = err.message;
        error.classList.remove('hidden');
    } finally {
        // Reset loading state
        submitBtn.disabled = false;
        submitText.style.display = 'inline';
        loadingText.classList.remove('active');
    }
});

function displayResults(data) {
    // Categoria: Produtivo em azul, Improdutivo em laranja, outro amarelo (pode ajustar)
    const categoryColor = data.category === 'Produtivo' ? 'green' : data.category === 'Improdutivo' ? 'red' : 'yellow';

    // Confiança: >= 80 azul, >= 60 laranja, abaixo laranja também (ou outra cor)
    const confidenceColor = data.confidence >= 70 ? 'green' : data.confidence <= 70 ? 'red' : 'orange';

    resultContent.innerHTML = `
        <div class="space-y-6">
            <!-- Classification -->
            <div class="flex items-center justify-between">
                <div class="flex items-center">
                    <i class="fas fa-tag text-${categoryColor}-600 mr-3"></i>
                    <div>
                        <h3 class="text-lg font-semibold">Classificação</h3>
                        <p class="text-sm text-gray-600">Categoria identificada pela IA</p>
                    </div>
                </div>
                <span class="px-3 py-1 bg-${categoryColor}-100 text-${categoryColor}-800 rounded-full text-sm font-medium">
                    ${data.category}
                </span>
            </div>
            
            <!-- Confidence -->
            <div class="flex items-center">
                <i class="fas fa-chart-line text-gray-400 mr-3"></i>
                <span class="text-sm text-gray-600 mr-2">Confiança:</span>
                <span class="text-sm font-semibold text-${confidenceColor}-600">${data.confidence}%</span>
                <div class="flex-1 ml-4">
                    <div class="bg-gray-200 rounded-full h-2">
                        <div class="h-2 rounded-full bg-${confidenceColor}-600" style="width: ${data.confidence}%"></div>
                    </div>
                </div>
            </div>
            
            <!-- Raciocínio -->
            <div class="bg-gray-50 rounded-lg p-4">
                <h4 class="font-medium text-gray-900 mb-2">
                    <i class="fas fa-lightbulb text-yellow-500 mr-2"></i>Raciocínio
                </h4>
                <p class="text-gray-700">${data.reasoning}</p>
            </div>
            
            <!-- Resposta Sugerida -->
            <div class="bg-blue-50 rounded-lg p-4">
                <h4 class="font-medium text-blue-900 mb-2">
                    <i class="fas fa-robot text-blue-600 mr-2"></i>Resposta Sugerida
                </h4>
                <div class="bg-white rounded p-3 border border-blue-200">
                    <p class="text-gray-800">${data.suggestedResponse}</p>
                </div>
                <button 
                    class="mt-2 text-sm text-blue-600 hover:text-blue-700 copy-btn"
                    data-response="${encodeURIComponent(data.suggestedResponse)}"
                >
                    <i class="fas fa-copy mr-1"></i>Copiar Resposta
                </button>
            </div>
            
            <!-- Metadata -->
            <div class="bg-gray-50 rounded-lg p-4 text-sm text-gray-600">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                    <div>
                        <strong>ID:</strong> ${data.id}
                    </div>
                    <div>
                        <strong>Processado em:</strong> ${new Date(data.timestamp).toLocaleString('pt-BR')}
                    </div>
                    ${data.fileName ? `<div><strong>Arquivo:</strong> ${data.fileName}</div>` : ''}
                </div>
            </div>
        </div>
    `;

    results.classList.remove('hidden');
}

document.addEventListener('click', function (e) {
    if (e.target.closest('.copy-btn')) {
        const btn = e.target.closest('.copy-btn');
        const text = decodeURIComponent(btn.getAttribute('data-response'));
        
        navigator.clipboard.writeText(text)
            .then(() => {
                alert('Resposta copiada para a área de transferência!');
            })
            .catch(() => {
                alert('Erro ao copiar a resposta. Verifique as permissões do navegador.');
            });
    }
});
