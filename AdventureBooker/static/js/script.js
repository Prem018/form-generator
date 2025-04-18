document.addEventListener('DOMContentLoaded', function() {
    // Initialize print functionality
    const printButtons = document.querySelectorAll('.btn-print');
    if (printButtons) {
        printButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Ensure all text inputs and textareas retain their values during printing
                document.querySelectorAll('input.text-field, input.date-field, textarea').forEach(input => {
                    // Add a data attribute with the value to ensure it's preserved for printing
                    if (input.value) {
                        input.setAttribute('data-value', input.value);
                    }
                });
                
                // Print the document
                window.print();
            });
        });
    }

    // Initialize data set switching
    const switchButtons = document.querySelectorAll('.btn-switch');
    if (switchButtons) {
        switchButtons.forEach(button => {
            button.addEventListener('click', function() {
                const currentUrl = new URL(window.location.href);
                const currentDataSet = currentUrl.searchParams.get('data_set') || 'set1';
                const newDataSet = currentDataSet === 'set1' ? 'set2' : 'set1';
                
                currentUrl.searchParams.set('data_set', newDataSet);
                window.location.href = currentUrl.toString();
            });
        });
    }
    
    // Enable editable rows in Medical Expense form
    const addRowButtons = document.querySelectorAll('.add-row-btn');
    if (addRowButtons) {
        addRowButtons.forEach(button => {
            button.addEventListener('click', function() {
                console.log("Add row button clicked");
                const tableId = this.getAttribute('data-table');
                console.log("Table ID:", tableId);
                
                // Find the correct table by looking through all tables in the document
                // and finding the one closest to this button
                let targetTable = null;
                
                // First, try to find a table that's a sibling before this button
                let prevElement = button.previousElementSibling;
                while (prevElement) {
                    if (prevElement.tagName && prevElement.tagName.toLowerCase() === 'table') {
                        targetTable = prevElement;
                        break;
                    }
                    prevElement = prevElement.previousElementSibling;
                }
                
                // If we didn't find a table, search more broadly
                if (!targetTable) {
                    // Look for the closest section containing this button
                    const section = button.closest('.section');
                    if (section) {
                        // Find the table within this section
                        targetTable = section.querySelector('table');
                    }
                }
                
                // If still no table, search even more broadly
                if (!targetTable) {
                    // Find all tables on the page
                    const allTables = document.querySelectorAll('table');
                    // Find the one closest to our button
                    let closestDistance = Infinity;
                    
                    allTables.forEach(table => {
                        const rect1 = button.getBoundingClientRect();
                        const rect2 = table.getBoundingClientRect();
                        const distance = Math.abs(rect1.top - rect2.bottom);
                        
                        if (distance < closestDistance) {
                            closestDistance = distance;
                            targetTable = table;
                        }
                    });
                }
                
                if (targetTable) {
                    console.log("Found target table:", targetTable);
                    addNewRow(targetTable);
                } else {
                    console.error("Could not find a table to add a row to");
                }
            });
        });
    }
    
    // Helper function to add a new row to a table
    function addNewRow(table) {
        const tableBody = table.querySelector('tbody');
        if (!tableBody) {
            console.error("No tbody found in table");
            return;
        }
        
        // Clone the last row template and clear its values
        const lastRow = tableBody.querySelector('tr:last-child');
        if (!lastRow) {
            console.error("No rows found in table");
            return;
        }
        
        const newRow = lastRow.cloneNode(true);
        console.log("Created new row");
        
        // Clear input values in the new row
        const inputs = newRow.querySelectorAll('input');
        inputs.forEach(input => {
            input.value = '';
        });
        
        tableBody.appendChild(newRow);
        console.log("Added new row to table");
    }
    
    // Handle checkbox toggles (radio-like behavior)
    const checkboxes = document.querySelectorAll('input[type="checkbox"].exclusive');
    if (checkboxes) {
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    const name = this.getAttribute('name');
                    const group = document.querySelectorAll(`input[name="${name}"]`);
                    
                    group.forEach(item => {
                        if (item !== this) {
                            item.checked = false;
                        }
                    });
                }
            });
        });
    }
    
    // Make pain scale behave like radio buttons
    const painScaleInputs = document.querySelectorAll('.pain-scale input');
    if (painScaleInputs) {
        painScaleInputs.forEach(input => {
            input.addEventListener('change', function() {
                if (this.checked) {
                    painScaleInputs.forEach(item => {
                        if (item !== this) {
                            item.checked = false;
                        }
                    });
                }
            });
        });
    }
});