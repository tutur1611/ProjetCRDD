document.addEventListener("DOMContentLoaded", function () {
    const figuresDropdown = document.getElementById("figures");
    const dynamicForm = document.getElementById("dynamic-form");

    // Liste des lettres disponibles
    const lettresList = ['H', 'S', 'E', 'V', 'K', 'A', 'F', 'P', 'B', 'R', 'M', 'C'];

    // Fonction pour créer une liste déroulante avec les lettres
    function createLetterDropdown(id) {
        let options = lettresList.map(letter => `<option value="${letter}">${letter}</option>`).join('');
        return `<select class="form-select mb-2" id="${id}">${options}</select>`;
    }

    // Fonction pour créer un bloc de sélection pour une figure
    function createSelectionBlock(index) {
        return `
            <div class="mb-3" id="figure-block-${index}">
                <label>Figure ${index}</label>
                <select class="form-select mb-2 figure-type" id="figure-${index}" data-index="${index}">
                    <option value="Doubler">Doubler</option>
                    <option value="Diagonale">Diagonale</option>
                    <option value="Volte">Volte</option>
                    <option value="Petite Volte">Petite Volte</option>
                </select>
                <label for="depart-${index}">Lettre de départ</label>
                ${createLetterDropdown(`depart-${index}`)}
                <label for="arrive-${index}" class="arrive-label">Lettre d'arrivée</label>
                ${createLetterDropdown(`arrive-${index}`)}
            </div>
        `;
    }

    // Fonction pour gérer l'affichage des champs en fonction du type de figure
    function handleFigureTypeChange(event) {
        const selectElement = event.target;
        const index = selectElement.dataset.index;
        const arriveField = document.getElementById(`arrive-${index}`);
        const arriveLabel = document.querySelector(`#figure-block-${index} .arrive-label`);

        // Afficher ou masquer le champ "Lettre d'arrivée" en fonction du type
        if (selectElement.value === "Doubler" || selectElement.value === "Diagonale") {
            arriveField.style.display = "block";
            arriveLabel.style.display = "block";
        } else {
            arriveField.style.display = "none";
            arriveLabel.style.display = "none";
        }
    }

    // Met à jour le formulaire dynamique en fonction du nombre de figures
    figuresDropdown.addEventListener("change", function () {
        const numberOfFigures = parseInt(figuresDropdown.value, 10);
        dynamicForm.innerHTML = "";

        for (let i = 1; i <= numberOfFigures; i++) {
            dynamicForm.innerHTML += createSelectionBlock(i);
        }

        // Ajouter des écouteurs pour chaque type de figure
        const figureTypeSelectors = document.querySelectorAll(".figure-type");
        figureTypeSelectors.forEach(selector => {
            selector.addEventListener("change", handleFigureTypeChange);
            selector.dispatchEvent(new Event("change")); // Déclenche un événement pour appliquer l'état initial
        });
    });

    // Déclencher un événement initial pour afficher le formulaire par défaut
    figuresDropdown.dispatchEvent(new Event("change"));
});
