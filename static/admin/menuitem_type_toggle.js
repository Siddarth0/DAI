document.addEventListener('DOMContentLoaded', function () {
    const typeSelect = document.getElementById('id_type');
    const internalField = document.querySelector('.form-row.field-internal_link');
    const cmsField = document.querySelector('.form-row.field-cms_link');
    const externalField = document.querySelector('.form-row.field-external_link');

    function toggleFields() {
        const type = typeSelect.value;

        internalField.style.display = 'none';
        cmsField.style.display = 'none';
        externalField.style.display = 'none';

        if (type === 'internal') {
            internalField.style.display = 'block';
        } else if (type === 'cms') {
            cmsField.style.display = 'block';
        } else if (type === 'external') {
            externalField.style.display = 'block';
        }
    }

    if (typeSelect) {
        typeSelect.addEventListener('change', toggleFields);
        toggleFields(); // run on page load
    }
});
