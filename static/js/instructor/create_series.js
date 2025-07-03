// Variables globales
    let selectedPostures = [];
    let availablePostures = [];
    
    document.addEventListener('DOMContentLoaded', function() {
        const therapyTypeSelect = document.getElementById('therapy_type');
        const posturesSection = document.getElementById('posturesSection');
        const postureList = document.getElementById('postureList');
        const selectedPosturesList = document.getElementById('selectedPosturesList');
        const selectedPosturesContainer = document.getElementById('selectedPostures');
        const submitBtn = document.getElementById('submitBtn');
        const posturesDataInput = document.getElementById('postures_data');
        
        // Escuchar selección de tipo de terapia
        therapyTypeSelect.addEventListener('change', function() {
            const therapyId = this.value;
            if (therapyId) {
                // Obtener posturas para el tipo de terapia seleccionado
                fetch(`/instructor/therapy/${therapyId}/postures`)
                    .then(response => response.json())
                    .then(data => {
                        availablePostures = data.postures;
                        renderAvailablePostures();
                        posturesSection.style.display = 'block';
                    })
                    .catch(error => console.error('Error al obtener posturas:', error));
            } else {
                posturesSection.style.display = 'none';
                selectedPostures = [];
                updateSelectedPosturesList();
            }
        });
        
        // Función para mostrar posturas disponibles (VERSIÓN CORREGIDA)
        function renderAvailablePostures() {
            postureList.innerHTML = '';
            
            availablePostures.forEach(posture => {
                const isSelected = selectedPostures.some(p => p.id === posture.id);
                
                const postureCard = document.createElement('div');
                postureCard.className = `posture-card ${isSelected ? 'selected' : ''}`;
                postureCard.dataset.id = posture.id;
                
                // Detectar si es video de YouTube
                const isYouTube = posture.image_url && 
                                 (posture.image_url.includes('youtube.com') || 
                                  posture.image_url.includes('youtu.be'));
                
                // Extraer ID de YouTube
                let videoContent = '';
                if (isYouTube) {
                    const videoId = posture.image_url.split('v=')[1]?.split('&')[0] || 
                                   posture.image_url.split('youtu.be/')[1]?.split('?')[0];
                    videoContent = `
                        <iframe 
                            src="https://www.youtube.com/embed/${videoId}?rel=0&modestbranding=1" 
                            frameborder="0" 
                            allowfullscreen>
                        </iframe>`;
                } else {
                    videoContent = `<img src="${posture.image_url || '/static/images/pose-placeholder.jpg'}" alt="${posture.name}">`;
                }
                
                postureCard.innerHTML = `
                    <div class="posture-image">
                        ${videoContent}
                    </div>
                    <div class="posture-details">
                        <div class="posture-name">${posture.name}</div>
                        <div class="posture-sanskrit">${posture.sanskrit_name || ''}</div>
                    </div>
                `;
                
                postureCard.addEventListener('click', function() {
                    const postureId = parseInt(this.dataset.id);
                    
                    if (isSelected) {
                        selectedPostures = selectedPostures.filter(p => p.id !== postureId);
                        this.classList.remove('selected');
                    } else {
                        const postureToAdd = availablePostures.find(p => p.id === postureId);
                        selectedPostures.push({
                            ...postureToAdd,
                            duration: 2
                        });
                        this.classList.add('selected');
                    }
                    
                    updateSelectedPosturesList();
                    updateFormData();
                });
                
                postureList.appendChild(postureCard);
            });
        }
        
        // Función para actualizar la lista de posturas seleccionadas
        function updateSelectedPosturesList() {
            selectedPosturesList.innerHTML = '';
            
            if (selectedPostures.length === 0) {
                selectedPosturesContainer.style.display = 'none';
                submitBtn.style.display = 'none';
                return;
            }
            
            selectedPosturesContainer.style.display = 'block';
            submitBtn.style.display = 'block';
            
            selectedPostures.forEach((posture, index) => {
                const postureItem = document.createElement('div');
                postureItem.className = 'selected-posture';
                
                postureItem.innerHTML = `
                    <span class="posture-number">${index + 1}.</span>
                    <span class="posture-name">${posture.name}</span>
                    <div class="posture-duration">
                        <input type="number" min="1" max="20" value="${posture.duration}" data-id="${posture.id}"> min
                    </div>
                    <div class="reorder-controls">
                        <button type="button" class="reorder-btn move-up" ${index === 0 ? 'disabled' : ''}>↑</button>
                        <button type="button" class="reorder-btn move-down" ${index === selectedPostures.length - 1 ? 'disabled' : ''}>↓</button>
                    </div>
                    <button type="button" class="remove-posture">×</button>
                `;
                
                // Evento para cambiar duración
                const durationInput = postureItem.querySelector('.posture-duration input');
                durationInput.addEventListener('change', function() {
                    const postureId = parseInt(this.dataset.id);
                    const duration = parseInt(this.value) || 1;
                    
                    // Actualizar duración en selectedPostures
                    selectedPostures = selectedPostures.map(p => {
                        if (p.id === postureId) {
                            return { ...p, duration };
                        }
                        return p;
                    });
                    
                    updateFormData();
                });
                
                // Botón mover arriba
                const moveUpBtn = postureItem.querySelector('.move-up');
                moveUpBtn.addEventListener('click', function() {
                    if (index > 0) {
                        const temp = selectedPostures[index];
                        selectedPostures[index] = selectedPostures[index - 1];
                        selectedPostures[index - 1] = temp;
                        updateSelectedPosturesList();
                        updateFormData();
                    }
                });
                
                // Botón mover abajo
                const moveDownBtn = postureItem.querySelector('.move-down');
                moveDownBtn.addEventListener('click', function() {
                    if (index < selectedPostures.length - 1) {
                        const temp = selectedPostures[index];
                        selectedPostures[index] = selectedPostures[index + 1];
                        selectedPostures[index + 1] = temp;
                        updateSelectedPosturesList();
                        updateFormData();
                    }
                });
                
                // Botón eliminar
                const removeBtn = postureItem.querySelector('.remove-posture');
                removeBtn.addEventListener('click', function() {
                    selectedPostures = selectedPostures.filter((_, i) => i !== index);
                    
                    // Actualizar estado de selección en la tarjeta
                    const postureCard = document.querySelector(`.posture-card[data-id="${posture.id}"]`);
                    if (postureCard) {
                        postureCard.classList.remove('selected');
                    }
                    
                    updateSelectedPosturesList();
                    updateFormData();
                });
                
                selectedPosturesList.appendChild(postureItem);
            });
        }
        
        // Función para actualizar los datos del formulario
        function updateFormData() {
            // Preparar datos para enviar
            const formData = selectedPostures.map(posture => ({
                id: posture.id,
                duration: posture.duration
            }));
            
            posturesDataInput.value = JSON.stringify(formData);
        }
        
        // Envío del formulario
        document.getElementById('createSeriesForm').addEventListener('submit', function(e) {
            if (selectedPostures.length === 0) {
                e.preventDefault();
                alert('Por favor seleccione al menos una postura para la serie.');
            }
        });
    });