document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM chargé !");

    const buttons = document.querySelectorAll('button');

    buttons.forEach((button) => {
        button.addEventListener('click', (event) => {
            if (button.disabled) return; // Empêche les doubles clics
            button.disabled = true; // Désactive le bouton après le premier clic
            setTimeout(() => {
                button.disabled = false; // Réactive le bouton après un délai
            }, 1000); // Délai de 1 seconde
        });
    });
});

console.log("Script chargé !");

function generateFigureForms() {
    console.log("generateFigureForms appelée !");
    const figureCountElement = document.getElementById('figureCount');
    const figureFormsContainer = document.getElementById('figureForms');
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');

    const figureCount = figureCountElement.value;

    if (!figureCount) {
        alert("Veuillez sélectionner un nombre de figures.");
        return;
    }

    figureFormsContainer.innerHTML = '';

    const dressageLetters = ['H', 'S', 'E', 'V', 'K', 'A', 'F', 'P', 'B', 'R', 'M', 'C'];
    const invalidStartCercle = ['K', 'F', 'M', 'H'];
    const validDoubler = {
        'A': ['C'], 'C': ['A'], 'K': ['F'], 'F': ['K'],
        'V': ['P'], 'P': ['V'], 'E': ['B'], 'B': ['E'],
        'S': ['R'], 'R': ['S'], 'H': ['M'], 'M': ['H']
    };
    const validDiagonale = {
        'M': ['K'], 
        'K': ['M'], 
        'F': ['H'], 
        'H': ['F']  
    };

    for (let i = 1; i <= figureCount; i++) {
        const formGroup = document.createElement('div');
        formGroup.className = 'mb-4 border p-3 rounded bg-light';

        formGroup.innerHTML = `
            <h6>Figure ${i}</h6>
            <div class="mb-3">
                <label for="figureType${i}" class="form-label">Type de Figure :</label>
                <select id="figureType${i}" class="form-select" required>
                    <option value="" disabled selected>Veuillez sélectionner...</option>
                    <option value="Volte">Volte</option>
                    <option value="Cercle">Cercle</option>
                    <option value="Doubler">Ligne droite</option>
                    <option value="Diagonale">Diagonale</option>
                </select>
            </div>
            <div class="mb-3">
                <label for="lettreDepart${i}" class="form-label">Lettre de Départ :</label>
                <select id="lettreDepart${i}" class="form-select" required>
                    <option value="" disabled selected>Veuillez sélectionner...</option>
                    ${dressageLetters.map(letter => `<option value="${letter}">${letter}</option>`).join('')}
                </select>
            </div>
            <div class="mb-3" id="lettreArriveeContainer${i}" style="display: none;">
                <label for="lettreArrivee${i}" class="form-label">Lettre d'Arrivée :</label>
                <select id="lettreArrivee${i}" class="form-select">
                    <option value="" disabled selected>Veuillez sélectionner...</option>
                </select>
            </div>
        `;

        figureFormsContainer.appendChild(formGroup);

        const figureType = document.getElementById(`figureType${i}`);
        const lettreDepart = document.getElementById(`lettreDepart${i}`);
        const lettreArriveeContainer = document.getElementById(`lettreArriveeContainer${i}`);
        const lettreArrivee = document.getElementById(`lettreArrivee${i}`);

        figureType.addEventListener('change', () => {
            const type = figureType.value;

            if (type === 'Volte') {
                lettreArriveeContainer.style.display = 'none';
                lettreDepart.innerHTML = `
                    <option value="" disabled selected>Veuillez sélectionner...</option>
                    ${dressageLetters.map(letter => `<option value="${letter}">${letter}</option>`).join('')}
                `;
            } else if (type === 'Cercle') {
                lettreArriveeContainer.style.display = 'none';
                lettreDepart.innerHTML = `
                    <option value="" disabled selected>Veuillez sélectionner...</option>
                    ${dressageLetters
                        .filter(letter => !invalidStartCercle.includes(letter)) // Exclure K, F, M, H
                        .map(letter => `<option value="${letter}">${letter}</option>`)
                        .join('')}`;
            } else if (type === 'Doubler') {
                lettreArriveeContainer.style.display = 'block';
                lettreDepart.innerHTML = `
                    <option value="" disabled selected>Veuillez sélectionner...</option>
                    ${Object.keys(validDoubler) 
                        .map(letter => `<option value="${letter}">${letter}</option>`)
                        .join('')}`;
                lettreDepart.addEventListener('change', () => {
                    const start = lettreDepart.value;
                    const validArrivals = validDoubler[start] || [];
                    lettreArrivee.innerHTML = `
                        <option value="" disabled selected>Veuillez sélectionner...</option>
                        ${validArrivals.map(letter => `<option value="${letter}">${letter}</option>`).join('')}`;
                });
                lettreDepart.dispatchEvent(new Event('change'));
            } else if (type === 'Diagonale') {
                lettreArriveeContainer.style.display = 'block';
                lettreDepart.innerHTML = `
                    <option value="" disabled selected>Veuillez sélectionner...</option>
                    ${Object.keys(validDiagonale) 
                        .map(letter => `<option value="${letter}">${letter}</option>`)
                        .join('')}`;
                lettreDepart.addEventListener('change', () => {
                    const start = lettreDepart.value;
                    const validArrivals = validDiagonale[start] || [];
                    lettreArrivee.innerHTML = `
                        <option value="" disabled selected>Veuillez sélectionner...</option>
                        ${validArrivals.map(letter => `<option value="${letter}">${letter}</option>`).join('')}`;
                });
                lettreDepart.dispatchEvent(new Event('change'));
            }
        });

        figureType.dispatchEvent(new Event('change'));
    }

    step1.style.display = 'none';
    step2.style.display = 'block';
}

function saveReprise() {
    console.log("saveReprise appelée !");
    const figureCountElement = document.getElementById('figureCount');
    const figureCount = figureCountElement.value;
    const figures = [];

    for (let i = 1; i <= figureCount; i++) {
        const type = document.getElementById(`figureType${i}`).value;
        const lettreDepart = document.getElementById(`lettreDepart${i}`).value.toUpperCase();
        const lettreArrivee = document.getElementById(`lettreArrivee${i}`).value.toUpperCase();

        if (!lettreDepart) {
            alert(`La lettre de départ est obligatoire pour la figure ${i}.`);
            return;
        }

        figures.push({ type, lettreDepart, lettreArrivee });
    }

    const repriseName = prompt("Entrez un nom pour la reprise :");
    if (!repriseName) {
        alert("Le nom de la reprise est obligatoire.");
        return;
    }

    fetch('/save_reprise', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nom: repriseName, figures }),
    })
    .then(response => response.json())
    .then(data => {
        window.location.reload();
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}

function generateGraph() {
    console.log("generateGraph appelée !");
    const figureCountElement = document.getElementById('figureCount');
    const figureCount = figureCountElement.value;
    const figures = [];

    for (let i = 1; i <= figureCount; i++) {
        const type = document.getElementById(`figureType${i}`).value;
        const lettreDepart = document.getElementById(`lettreDepart${i}`).value.toUpperCase();
        const lettreArrivee = document.getElementById(`lettreArrivee${i}`).value.toUpperCase();

        if (!lettreDepart) {
            alert(`La lettre de départ est obligatoire pour la figure ${i}.`);
            return;
        }

        figures.push({ type, start: lettreDepart, end: lettreArrivee });
    }

    fetch('/generate_graph', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ figures }),
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        } else {
            throw new Error('Erreur lors de la génération du graphique.');
        }
    })
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const img = document.createElement('img');
        img.src = url;
        img.alt = 'Graphique de la reprise';
        document.getElementById('graphContainer').innerHTML = '';
        document.getElementById('graphContainer').appendChild(img);
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert("Une erreur s'est produite lors de la génération du graphique.");
    });
}