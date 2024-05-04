// Lấy dữ liệu nhà cung cấp từ API
fetch('/Supplier')
    .then(response => response.json())
    .then(data => {
        const tbody = document.querySelector('tbody');
        data.forEach((supplier, index) => {
            const row = tbody.insertRow();
            row.insertCell().textContent = index + 1;
            row.insertCell().textContent = supplier.SupplierName;
            row.insertCell().textContent = supplier.AccountName;
            row.insertCell().textContent = supplier.EmailAddress;
            row.insertCell().textContent = supplier.Tel;
            row.insertCell().textContent = supplier.Location;
        });
    });

const deleteButtons = document.querySelectorAll('.delete-button');

deleteButtons.forEach(button => {
    button.addEventListener('click', () => {
        const supplierId = button.dataset.supplierId;
        const url = `/Supplier?id=${supplierId}`;

        fetch(url, { method: 'DELETE' })
        .then(response => {
            if (response.ok) {
                // Success - Remove supplier row from the table
                button.parentNode.parentNode.remove(); 
            } else {
                response.json().then(data => alert(data.error));
            }
        })
        .catch(error => console.error('Error:', error)); 
    });
});