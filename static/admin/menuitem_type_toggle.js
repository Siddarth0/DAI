document.addEventListener('DOMContentLoaded', function () {
    const typeSelect = document.getElementById('id_type');
    const internalField = document.querySelector('.form-row.field-internal_link');
    const cmsField = document.querySelector('.form-row.field-cms_link');
    const externalField = document.querySelector('.form-row.field-external_link');

    function toggleLinkFields() {
        const selectedType = typeSelect.value;
        if (selectedType === 'internal') {
            internalField.style.display = '';
            cmsField.style.display = 'none';
            externalField.style.display = 'none';
        } else if (selectedType === 'cms') {
            internalField.style.display = 'none';
            cmsField.style.display = '';
            externalField.style.display = 'none';
        } else if (selectedType === 'external') {
            internalField.style.display = 'none';
            cmsField.style.display = 'none';
            externalField.style.display = '';
        } else {
            internalField.style.display = 'none';
            cmsField.style.display = 'none';
            externalField.style.display = 'none';
        }
    }

    typeSelect.addEventListener('change', toggleLinkFields);
    toggleLinkFields();  // run on page load
});
