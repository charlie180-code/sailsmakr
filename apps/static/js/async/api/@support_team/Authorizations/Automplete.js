import domain from "../../../../_globals/domain.js";

const company_id = document.querySelector('#company_id').value;

function debounce(func, delay) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), delay);
    };
}

const autocompleteFields = [
    { id: 'clientLastName', field: 'client_last_name', datalist: 'clientLastNameSuggestions' },
    { id: 'clientFirstName', field: 'client_first_name', datalist: 'clientFirstNameSuggestions' },
    { id: 'clientLocation', field: 'client_location', datalist: 'clientLocationSuggestions' },
    { id: 'clientPhone', field: 'client_phone_number', datalist: 'clientPhoneSuggestions' },
    { id: 'billsOfLading', field: 'lading_bills_identifier', datalist: 'billsOfLadingSuggestions' },
    { id: 'agentLastName', field: 'agent_last_name', datalist: 'agentLastNameSuggestions' },
    { id: 'agentFirstName', field: 'agent_first_name', datalist: 'agentFirstNameSuggestions' },
    { id: 'company_proof_nif', field: 'company_proof_nif', datalist: 'companyNifSuggestions' },
    { id: 'company_proof_rccm', field: 'company_proof_rccm', datalist: 'companyRccmSuggestions' },
    { id: 'companyName', field: 'company_name', datalist: 'companyNameSuggestions' }
];

autocompleteFields.forEach(item => {
    const input = document.getElementById(item.id);
    if (input) {
        const debouncedInput = debounce(function(e) {
            const searchTerm = e.target.value;
            if (searchTerm.length < 2) return;
            
            fetch(`${domain}/order/v1/search-authorizations/${company_id}?term=${encodeURIComponent(searchTerm)}&field=${item.field}`)
                .then(response => response.json())
                .then(data => {
                    const datalist = document.getElementById(item.datalist);
                    if (datalist) {
                        datalist.innerHTML = '';
                        
                        data.forEach(auth => {
                            const option = document.createElement('option');
                            option.value = auth[item.field] || '';
                            option.dataset.json = JSON.stringify(auth);
                            datalist.appendChild(option);
                        });
                    }
                })
                .catch(error => console.error('Autocomplete error:', error));
        }, 300);

        input.addEventListener('input', debouncedInput);
        
        input.addEventListener('change', function(e) {
            const datalist = document.getElementById(item.datalist);
            if (!datalist) return;
            
            const selectedOption = Array.from(datalist.options).find(option => option.value === e.target.value);
            if (selectedOption && selectedOption.dataset.json) {
                try {
                    const data = JSON.parse(selectedOption.dataset.json);
                    autocompleteFields.forEach(field => {
                        if (field.id !== item.id && data[field.field]) {
                            const el = document.getElementById(field.id);
                            if (el) el.value = data[field.field];
                        }
                    });
                } catch (e) {
                    console.error('Error parsing autocomplete data:', e);
                }
            }
        });
    }
});