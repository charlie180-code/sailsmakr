import domain from "../../../../_globals/domain.js";

const company_id = document.querySelector('#company_id').value


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
    { id: 'clientLastName', field: 'client_last_name' },
    { id: 'clientFirstName', field: 'client_first_name' },
    { id: 'clientLocation', field: 'client_location' },
    { id: 'clientPhone', field: 'client_phone_number' },
    { id: 'billsOfLading', field: 'lading_bills_identifier' },
    { id: 'agentLastName', field: 'agent_last_name' },
    { id: 'agentFirstName', field: 'agent_first_name' },
    { id: 'company_proof_nif', field: 'company_proof_nif' },
    { id: 'company_proof_rccm', field: 'company_proof_rccm' }
];

autocompleteFields.forEach(item => {
    const input = document.getElementById(item.id);
    if (input) {
        input.addEventListener('input', function(e) {
            const searchTerm = e.target.value;
            if (searchTerm.length < 2) return;
            
            fetch(`${domain}/order/v1/search-authorizations/${company_id}?term=${encodeURIComponent(searchTerm)}&field=${item.field}`)
                .then(response => response.json())
                .then(data => {
                    const datalist = document.getElementById(`${item.id}Suggestions`);
                    datalist.innerHTML = '';
                    
                    data.forEach(auth => {
                        const option = document.createElement('option');
                        option.value = auth[item.field] || '';
                        option.dataset.json = JSON.stringify(auth);
                        datalist.appendChild(option);
                    });
                });
        });
        
        input.addEventListener('change', function(e) {
            const selectedOption = document.querySelector(`#${item.id}Suggestions option[value="${e.target.value}"]`);
            if (selectedOption) {
                const data = JSON.parse(selectedOption.dataset.json);
                autocompleteFields.forEach(field => {
                    if (field.id !== item.id && data[field.field]) {
                        const el = document.getElementById(field.id);
                        if (el) el.value = data[field.field];
                    }
                });
            }
        });
    }
});