let barcodeBuffer = "";

document.body.addEventListener("keydown", function (e) {
    // Check if the pressed key is a printable character
    // console.log("eeeID",e.target.id);
    if (e.key.length === 1 && e.target.id === "barcode-number" ) {
        // console.log("heee")
        barcodeBuffer += e.key;
    } else if (e.key === "Enter" && e.target.id === "barcode-number") {
        // Move to the next section (amount section)
        document.getElementById('amount').focus();

        // Send the scanned barcode to the Flask backend
        sendBarcodeToBackend(barcodeBuffer);

        // Optionally, you can do something with the scanned barcode value
        // console.log('Scanned Barcode:', barcodeBuffer);
        // Reset the barcode buffer for the next scan
        barcodeBuffer = "";
    }
}, true);

function resetForm() {
    document.getElementById('barcode-number').value = '';
    document.getElementById('amount').value = '';
    document.getElementById('remain').value = '';  // Assuming 'remain' is an input field, not a text content
    document.getElementById('pdt-name').value = '';
    document.getElementById('item-number').value = '';
}

function sendBarcodeToBackend(barcode) {
    // Make an AJAX request to the Flask backend
    //console.log('sendBarcodeToBackend', barcode);
    fetch(`/get_values/${barcode}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // console.log('yoo',data);  // Log the response from the backend
        const remainElement = document.getElementById('remain');
        remainElement.value = String(data.remain_first);
        document.getElementById('item-number').value = String(data.item_number);
        document.getElementById('pdt-name').value = String(data.product_name);
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle the error as needed
    });
}

function appendToAmount(value) {
    document.getElementById('amount').value += value;
}

function backspace() {
    const amountInput = document.getElementById('amount');
    amountInput.value = amountInput.value.slice(0, -1);
}

function submitForm() {
    const barcodeNumber = document.getElementById('barcode-number').value;
    const amount = document.getElementById('amount').value;

    // console.log('Amount:', amount);
    // Make an AJAX request to the Flask backend to update values
    const parsedAmount = parseFloat(amount);
    if (isNaN(parsedAmount)) {
        console.error('Invalid amount. Please enter a valid number.');
        return;
    }

    // Make an AJAX request to the Flask backend to update values
    fetch('/update_values', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            barcode_number: barcodeNumber,
            amount: amount,
        }),
    })
    .then(response => response.json())
    .then(data => {
        try {
            const parsedData = JSON.parse(JSON.stringify(data));
            // console.log('Parsed Data: ', parsedData)
             // Update 'remain' section in the frontend
            // const remainElement = document.getElementById('remain');
            // remainElement.value = String(parsedData.amount_second);

        } catch(error){
            console.error('Error Parsing: ',data);
        }
        
        document.getElementById('amount').value = '';
        // console.log('Additional Information:', 'You can add more logs here if needed');
    })
    .catch(error => console.error('Error:', error));

    resetForm();
    document.getElementById('barcode-number').focus();
}



window.addEventListener('beforeunload', function () {
    resetForm();
});
