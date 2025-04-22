document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM chargé !");

    // Récupérer les éléments HTML
    const nextButton = document.getElementById('nextButton');
    const saveButton = document.getElementById('saveButton');
    const generateButton = document.getElementById('generateButton');

    // Gestion du clic sur le bouton "Suivant"
    nextButton.addEventListener('click', generateFigureForms);

    // Gestion du clic sur le bouton "Enregistrer la Reprise"
    saveButton.addEventListener('click', saveReprise);

    // Gestion du clic sur le bouton "Générer le Graphique"
    generateButton.addEventListener('click', generateGraph);
});

console.log("Script chargé !");

// Fonction pour générer les formulaires dynamiques
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

    // Réinitialiser le conteneur des formulaires
    figureFormsContainer.innerHTML = '';

    // Lettres disponibles pour une carrière de dressage
    const dressageLetters = ['H', 'S', 'E', 'V', 'K', 'A', 'F', 'P', 'B', 'R', 'M', 'C'];
    const invalidStartCercle = ['K', 'F', 'M', 'H'];
    const validDoubler = {
        'A': ['C'], 'C': ['A'], 'K': ['F'], 'F': ['K'],
        'V': ['P'], 'P': ['V'], 'E': ['B'], 'B': ['E'],
        'S': ['R'], 'R': ['S'], 'H': ['M'], 'M': ['H']
    };
    const validDiagonale = {
        'M': ['K'], // M peut aller vers K
        'K': ['M'], // K peut aller vers M
        'F': ['H'], // F peut aller vers H
        'H': ['F']  // H peut aller vers F
    };

    // Générer les formulaires pour chaque figure
    for (let i = 1; i <= figureCount; i++) {
        const formGroup = document.createElement('div');
        formGroup.className = 'mb-4 border p-3 rounded bg-light';

        formGroup.innerHTML = `
            <h6>Figure ${i}</h6>
            <div class="mb-3">
                <label for="figureType${i}" class="form-label">Type de Figure :</label>
                <select id="figureType${i}" class="form-select" required>
                    <option value="Volte">Volte</option>
                    <option value="Cercle">Cercle</option>
                    <option value="Doubler">Ligne droite</option>
                    <option value="Diagonale">Diagonale</option>
                </select>
            </div>
            <div class="mb-3">
                <label for="lettreDepart${i}" class="form-label">Lettre de Départ :</label>
                <select id="lettreDepart${i}" class="form-select" required>
                    ${dressageLetters.map(letter => `<option value="${letter}">${letter}</option>`).join('')}
                </select>
            </div>
            <div class="mb-3" id="lettreArriveeContainer${i}" style="display: none;">
                <label for="lettreArrivee${i}" class="form-label">Lettre d'Arrivée :</label>
                <select id="lettreArrivee${i}" class="form-select"></select>
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
                lettreDepart.innerHTML = dressageLetters
                    .map(letter => `<option value="${letter}">${letter}</option>`)
                    .join('');
            } else if (type === 'Cercle') {
                lettreArriveeContainer.style.display = 'none';
                lettreDepart.innerHTML = dressageLetters
                    .filter(letter => !invalidStartCercle.includes(letter)) // Exclure K, F, M, H
                    .map(letter => `<option value="${letter}">${letter}</option>`)
                    .join('');
            } else if (type === 'Doubler') {
                lettreArriveeContainer.style.display = 'block';
                lettreDepart.innerHTML = Object.keys(validDoubler) // Proposer uniquement les lettres valides pour doubler
                    .map(letter => `<option value="${letter}">${letter}</option>`)
                    .join('');
                lettreDepart.addEventListener('change', () => {
                    const start = lettreDepart.value;
                    const validArrivals = validDoubler[start] || [];
                    lettreArrivee.innerHTML = validArrivals
                        .map(letter => `<option value="${letter}">${letter}</option>`)
                        .join('');
                });
                lettreDepart.dispatchEvent(new Event('change'));
            } else if (type === 'Diagonale') {
                lettreArriveeContainer.style.display = 'block';
                lettreDepart.innerHTML = Object.keys(validDiagonale) // Proposer uniquement K, F, M, H
                    .map(letter => `<option value="${letter}">${letter}</option>`)
                    .join('');
                lettreDepart.addEventListener('change', () => {
                    const start = lettreDepart.value;
                    const validArrivals = validDiagonale[start] || [];
                    lettreArrivee.innerHTML = validArrivals
                        .map(letter => `<option value="${letter}">${letter}</option>`)
                        .join('');
                });
                lettreDepart.dispatchEvent(new Event('change'));
            }
        });

        figureType.dispatchEvent(new Event('change'));
    }

    step1.style.display = 'none';
    step2.style.display = 'block';
}

// Fonction pour enregistrer la reprise
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

    // Envoyer les données au serveur
    fetch('/save_reprise', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nom: repriseName, figures }),
    })
    .then(response => response.json())
    .then(data => {
        alert("Reprise enregistrée avec succès !");
        window.location.reload();
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert("Une erreur s'est produite lors de l'enregistrement.");
    });
}

// Fonction pour générer le graphique
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