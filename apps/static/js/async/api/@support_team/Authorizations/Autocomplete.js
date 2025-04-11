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
    { id: 'companyPhone', field: 'client_phone_number', displayField: 'client_phone_number_display', datalist: 'clientPhoneSuggestions' },
    { id: 'agentLastName', field: 'agent_last_name', datalist: 'agentLastNameSuggestions' },
    { id: 'agentFirstName', field: 'agent_first_name', datalist: 'agentFirstNameSuggestions' },
    { id: 'companyPhone', field: 'client_phone_number', displayField: 'client_phone_number_display', datalist: 'companyPhoneSuggestions'},
    { id: 'companyNif', field: 'company_proof_nif', displayField: 'company_proof_nif_display', datalist: 'companyNifSuggestions' },
    { id: 'companyRccm', field: 'company_proof_rccm', displayField: 'company_proof_rccm_display', datalist: 'companyRccmSuggestions' },
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
                            option.value = item.displayField ? auth[item.displayField] || auth[item.field] : auth[item.field] || '';
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
            
            const selectedOption = Array.from(datalist.options).find(option => {
                const optionValue = option.value.split(' - ')[0];
                const inputValue = e.target.value.split(' - ')[0];
                return optionValue === inputValue;
            });
            
            if (selectedOption && selectedOption.dataset.json) {
                try {
                    const data = JSON.parse(selectedOption.dataset.json);
                    autocompleteFields.forEach(field => {
                        if (field.id !== item.id && data[field.field]) {
                            const el = document.getElementById(field.id);
                            if (el) {
                                if (field.displayField && data[field.displayField]) {
                                    el.value = data[field.displayField];
                                } else {
                                    el.value = data[field.field];
                                }
                            }
                        }
                    });
                } catch (e) {
                    console.error('Error parsing autocomplete data:', e);
                }
            }
        });
    }
});