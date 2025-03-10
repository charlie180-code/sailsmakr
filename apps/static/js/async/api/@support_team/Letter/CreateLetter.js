import { showLoadingState, revertToOriginalState } from '../../../../UI/StatusHelpers.js';
import validateField from '../../../../UI/ValidationHelpers.js';
import domain from '../../../../_globals/domain.js';


const formId = "createLetterForm";
const submitButtonId = "SubmitButton";
const spinnerId = "Spinner";
const buttonIconId = "ButtonIcon";
const endpoint = `${domain}/order/v1/create_new_container_release_letter`;

document.getElementById(submitButtonId).addEventListener("click", async function (event) {
    event.preventDefault();
    const formId = "createLetterForm";
    const submitButtonId = "SubmitButton";
    const spinnerId = "Spinner";
    const buttonIconId = "ButtonIcon";
    const endpoint = `${domain}/order/v1/create_new_container_release_letter`;

    function customValidation(value) {
        return value.trim() !== "";
    }
    
    let isFormValid = true;

    const fieldMappings = [
        { id: "client_last_name", errorId: "clientLastNameError" },
        { id: "client_first_name", errorId: "clientFirstNameError" },
        { id: "client_phone_number", errorId: "clientPhoneError" },
        { id: "client_location", errorId: "clientLocationError" },
        { id: "bills_of_ladding", errorId: "billsOfLadingError" },
        { id: "agent_last_name", errorId: "agentLastNameError" },
        { id: "agent_first_name", errorId: "agentFirstNameError" },
    ];

    fieldMappings.forEach(({ id, errorId }) => {
        const field = document.querySelector(`[name="${id}"]`);
        const errorText = document.getElementById(errorId);
        if (!validateField(field, errorText, customValidation)) {
            isFormValid = false;
        }
    });

    const privacyPolicy = document.getElementById("privacyPolicy");
    const privacyError = document.getElementById("privacyPolicyError");
    if (!privacyPolicy.checked) {
        privacyError.style.display = "block";
        isFormValid = false;
    } else {
        privacyError.style.display = "none";
    }

    if (isFormValid) {
        try {
            showLoadingState(submitButtonId, spinnerId, buttonIconId);

            const formData = new FormData(document.getElementById(formId));
            
            const response = await fetch(endpoint, {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error("Failed to generate PDF.");
            }

            const jsonData = JSON.parse(response.headers.get('X-JSON-Data'));

            const pdfFilename = jsonData.pdf_filename;
            const title = jsonData.title;
            const message = jsonData.message;

            const pdfBlob = await response.blob();
            const url = window.URL.createObjectURL(pdfBlob);
            const a = document.createElement("a");
            a.href = url;
            a.download = pdfFilename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            Swal.fire({
                title: title,
                text: message,
                icon: "success",
                confirmButtonText: jsonData.confirmButtonText || "OK"
            }).then(() => {
                location.reload();
            });

            revertToOriginalState(submitButtonId, spinnerId, buttonIconId);

        } catch (error) {
            console.error("Error:", error);
            revertToOriginalState(submitButtonId, spinnerId, buttonIconId);
            
            Swal.fire({
                title: "Error!",
                text: error.message || "An error occurred while generating the PDF.",
                icon: "error",
                confirmButtonText: "OK"
            });
        }
    }
});