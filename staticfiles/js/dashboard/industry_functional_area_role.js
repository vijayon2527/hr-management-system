  document.addEventListener('DOMContentLoaded', function () {
    // Attach change event listener for industry
    const industrySelect = document.getElementById("id_industry");
    if (industrySelect) {
        industrySelect.addEventListener("change", loadFunctionalAreas);
    }

    // Attach change event listener for functional area
    const functionalAreaSelect = document.getElementById("id_functional_area");
    if (functionalAreaSelect) {
        functionalAreaSelect.addEventListener("change", loadRoles);
    }
});

function loadFunctionalAreas() {
    const industryId = document.getElementById("id_industry").value;
    if (!industryId) return;

    fetch(`/super_admin/get-functional-areas/?industry_id=${industryId}`)
        .then(response => response.json())
        .then(data => {
            const functionalAreaSelect = document.getElementById("id_functional_area");
            functionalAreaSelect.innerHTML = '<option value="">Select Functional Area</option>';
            data.forEach(area => {
                functionalAreaSelect.innerHTML += `<option value="${area.id}">${area.name}</option>`;
            });
        })
        .catch(error => console.error('Error loading functional areas:', error));
}

function loadRoles() {
    const functionalAreaId = document.getElementById("id_functional_area").value;
    if (!functionalAreaId) return;

    fetch(`/super_admin/get-roles/?functional_area_id=${functionalAreaId}`)
        .then(response => response.json())
        .then(data => {
            const roleSelect = document.getElementById("id_role");
            roleSelect.innerHTML = '<option value="">Select Role</option>';
            data.forEach(role => {
                roleSelect.innerHTML += `<option value="${role.id}">${role.name}</option>`;
            });
        })
        .catch(error => console.error('Error loading roles:', error));
}
