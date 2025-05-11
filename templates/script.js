// File type selection handling
const fileTypeButtons = document.querySelectorAll('.file-type-btn');
const fileInput = document.getElementById('dataFile');

// Initialize Python editor when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initializePythonEditor();
    
    // Add table toggle functionality
    const toggleBtn = document.getElementById('toggleTable');
    const tableWrapper = document.getElementById('tableWrapper');

    toggleBtn.addEventListener('click', () => {
        toggleBtn.classList.toggle('collapsed');
        tableWrapper.classList.toggle('collapsed');
    });
});

function initializePythonEditor() {
    const editorContainer = document.getElementById('pythonEditor');
    if (!editorContainer) {
        console.error('Python editor container not found');
        return;
    }

    try {
        // Clear any existing content
        editorContainer.innerHTML = '';
        
        const editor = CodeMirror(editorContainer, {
            mode: 'python',
            theme: 'monokai',
            lineNumbers: true,
            indentUnit: 4,
            smartIndent: true,
            lineWrapping: true,
            autoCloseBrackets: true,
            matchBrackets: true,
            cursorBlinkRate: 530,
            cursorHeight: 0.85,
            extraKeys: {
                "Ctrl-Space": "autocomplete",
                "Tab": "indentMore",
                "Shift-Tab": "indentLess"
            },
            value: `# Your Python code here
# The data is available as a pandas DataFrame in the 'df' variable
# Store your result in the 'result' variable

# Example: Filter data where column value is greater than 100
# df = df[df['column_name'] > 100]

# Example: Group by and calculate mean
# result = df.groupby('category')['value'].mean()

# Example: Sort data
# result = df.sort_values('column_name', ascending=False)

# Return the modified DataFrame
result = df
`
        });

        // Store the editor instance
        window.pythonEditor = editor;

        // Force refresh and focus the editor
        editor.refresh();
        editor.focus();
        
        // Add click event to ensure editor gets focus
        editorContainer.addEventListener('click', (e) => {
            editor.focus();
        });

    } catch (error) {
        console.error('Error initializing CodeMirror:', error);
    }
}

fileTypeButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all buttons
        fileTypeButtons.forEach(btn => btn.classList.remove('active'));
        // Add active class to clicked button
        button.classList.add('active');
        
        // Update file input accept attribute based on selected type
        const fileType = button.dataset.type;
        switch(fileType) {
            case 'csv':
                fileInput.accept = '.csv';
                break;
            case 'excel':
                fileInput.accept = '.xlsx,.xls';
                break;
            case 'json':
                fileInput.accept = '.json';
                break;
            case 'sql':
                fileInput.accept = '.sql';
                break;
        }
    });
});

document.getElementById('dataFile').addEventListener('change', handleFileUpload);

async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        
        if (response) {
            if (file.name.endsWith('.sql')) {
                displaySQLContent(result.content);
            } else {
                displayData(result);
                updateMetrics(result);
            }
        } else {
            throw new Error(result.error || 'Upload failed');
        }
    } catch (error) {
        alert('Error uploading file: ' + error.message);
    }
}

function displaySQLContent(content) {
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = '';
    
    const tr = document.createElement('tr');
    const td = document.createElement('td');
    td.textContent = content;
    td.style.whiteSpace = 'pre-wrap';
    tr.appendChild(td);
    tableBody.appendChild(tr);
}

function displayData(result) {
    const tableHeader = document.getElementById('tableHeader');
    const tableBody = document.getElementById('tableBody');
    const pythonEditorContainer = document.getElementById('pythonEditorContainer');
    const tableWrapper = document.querySelector('.table-wrapper');
    
    // Add horizontal scrolling to table wrapper
    tableWrapper.style.overflowX = 'auto';
    tableWrapper.style.maxWidth = '100%';
    
    // Show Python editor when data is loaded
    pythonEditorContainer.style.display = 'block';
    
    // Store the data in localStorage
    try {
        const dataString = JSON.stringify(result);
        localStorage.setItem('currentData', dataString);
        
        // Only update originalData if it's not already set
        if (!localStorage.getItem('originalData')) {
            localStorage.setItem('originalData', dataString);
        }
        
        // Store the data in window variables
        window.originalData = result;
        window.currentData = result;
    } catch (error) {
        console.error('Error saving data to localStorage:', error);
    }
    
    // Clear existing content
    tableHeader.innerHTML = '';
    tableBody.innerHTML = '';

    if (result.columns && result.columns.length > 0) {
        // Create header row
        result.columns.forEach(header => {
            const th = document.createElement('th');
            const headerContainer = document.createElement('div');
            headerContainer.className = 'column-header';
            
            const headerText = document.createElement('span');
            headerText.textContent = header;
            
            const dropdownBtn = document.createElement('button');
            dropdownBtn.className = 'column-options-btn';
            dropdownBtn.innerHTML = '<ion-icon name="ellipsis-vertical"></ion-icon>';
            
            const dropdownMenu = document.createElement('div');
            dropdownMenu.className = 'column-options-menu';
            dropdownMenu.innerHTML = `
                <button onclick="sortColumn('${header}', 'asc')">
                    <ion-icon name="arrow-up-outline"></ion-icon>
                    Sort Ascending
                </button>
                <button onclick="sortColumn('${header}', 'desc')">
                    <ion-icon name="arrow-down-outline"></ion-icon>
                    Sort Descending
                </button>
                <button onclick="filterColumn('${header}')">
                    <ion-icon name="funnel-outline"></ion-icon>
                    Filter
                </button>
                <button onclick="deleteColumn('${header}')">
                    <ion-icon name="trash-outline"></ion-icon>
                    Delete Column
                </button>
                <button onclick="describeColumn('${header}')">
                    <ion-icon name="analytics-outline"></ion-icon>
                    Describe Column
                </button>
            `;
            
            headerContainer.appendChild(headerText);
            headerContainer.appendChild(dropdownBtn);
            headerContainer.appendChild(dropdownMenu);
            th.appendChild(headerContainer);
            tableHeader.appendChild(th);

            // Add click event listener to the dropdown button
            dropdownBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                // Close all other open menus
                document.querySelectorAll('.column-options-menu').forEach(menu => {
                    if (menu !== dropdownMenu) {
                        menu.style.display = 'none';
                    }
                });
                // Toggle current menu
                dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
            });
        });
        
        result.data.forEach(row => {
            const tr = document.createElement('tr');
            result.columns.forEach(header => {
                const td = document.createElement('td');
                td.textContent = row[header] || '';
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });

        // Add click event listener to document to close menus when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.column-options-btn')) {
                document.querySelectorAll('.column-options-menu').forEach(menu => {
                    menu.style.display = 'none';
                });
            }
        });
    }
}

// Load saved data when page loads
document.addEventListener('DOMContentLoaded', () => {
    const savedData = localStorage.getItem('currentData');
    if (savedData) {
        try {
            const data = JSON.parse(savedData);
            window.currentData = data;
            window.originalData = JSON.parse(localStorage.getItem('originalData') || '{}');
            displayData(data);
        } catch (error) {
            console.error('Error loading saved data:', error);
        }
    }
});

function updateMetrics(result) {
    document.getElementById('totalRecords').textContent = result.row_count;
    document.getElementById('lastUpdated').textContent = new Date().toLocaleDateString();
}

function sortColumn(columnName, direction) {
    const data = {
        columnName: columnName,
        direction: direction
    };

    fetch('http://localhost:5000/analysis/sort', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        displayData(result);
        updateMetrics(result);
    })
    .catch(error => {
        console.error('Error sorting data:', error);
        alert('Error sorting data: ' + error.message);
    });
}

async function describeColumn(columnName) {
    if (!columnName) {
        console.error('Column name is required');
        return;
    }

    // Create data object to send to backend
    const data = {
        columnName: columnName
    };

    // Show loading state
    const loadingModal = document.createElement('div');
    loadingModal.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: #1a1a1a;
        padding: 20px;
        border-radius: 8px;
        z-index: 1000;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        border: 1px solid #3a3a3a;
    `;
    loadingModal.textContent = 'Loading statistics...';
    document.body.appendChild(loadingModal);

    // Make API call to backend
    fetch('http://localhost:5000/analysis/describe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.error || 'Failed to get column statistics');
            });
        }
        return response.json();
    })
    .then(result => {
        // Remove loading modal
        document.body.removeChild(loadingModal);

        if (!result || !result.describe) {
            throw new Error('No statistics available for this column');
        }

        // Create modal popup
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #1a1a1a;
            padding: 20px;
            border-radius: 8px;
            z-index: 1000;
            min-width: 300px;
            max-width: 600px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            border: 1px solid #3a3a3a;
            opacity: 1;
            transition: opacity 0.3s ease;
        `;

        // Add header
        const header = document.createElement('div');
        header.style.cssText = `
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #3a3a3a;
        `;
        header.innerHTML = `
            <h3 style="margin: 0; color: #00bfff; font-size: 1.2em;">Column Statistics: ${columnName}</h3>
            <button class="close-btn" style="
                background: none;
                border: none;
                color: #ffffff;
                cursor: pointer;
                font-size: 20px;
                padding: 5px;
                transition: color 0.3s;
            ">×</button>
        `;

        // Add content
        const content = document.createElement('div');
        content.style.cssText = `
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
            background: #1a1a1a;
            border-radius: 4px;
        `;

        // Format stats with number formatting
        const formatValue = (value) => {
            if (typeof value === 'number') {
                return value.toFixed(2);
            }
            return value;
        };

        // Format the statistics
        const stats = Object.entries(result.describe).map(([key, value]) => {
            return `
                <div style="
                    display: flex;
                    justify-content: space-between;
                    padding: 8px;
                    border-bottom: 1px solid #3a3a3a;
                    transition: background 0.3s;
                ">
                    <strong style="color: #00bfff;">${key}:</strong>
                    <span style="color: #ffffff;">${formatValue(value)}</span>
                </div>
            `;
        }).join('');

        content.innerHTML = stats || '<div style="color: #ffffff; padding: 8px;">No statistics available for this column.</div>';

        // Add hover effect for stats rows
        content.querySelectorAll('div').forEach(div => {
            div.onmouseover = () => div.style.background = '#2a2a2a';
            div.onmouseout = () => div.style.background = 'transparent';
        });

        // Assemble modal
        modal.appendChild(header);
        modal.appendChild(content);
        document.body.appendChild(modal);

        // Add overlay with blur effect
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(3px);
            z-index: 999;
            transition: opacity 0.3s;
            opacity: 1;
        `;
        document.body.appendChild(overlay);

        // Close modal function with animation
        const closeModal = () => {
            modal.style.opacity = '0';
            overlay.style.opacity = '0';
            setTimeout(() => {
                if (modal.parentNode) {
                    document.body.removeChild(modal);
                }
                if (overlay.parentNode) {
                    document.body.removeChild(overlay);
                }
            }, 300);
        };

        // Add hover effect for close button
        const closeBtn = modal.querySelector('.close-btn');
        closeBtn.onmouseover = () => closeBtn.style.color = '#00bfff';
        closeBtn.onmouseout = () => closeBtn.style.color = '#ffffff';

        // Add close handlers
        modal.querySelector('.close-btn').addEventListener('click', closeModal);
        overlay.addEventListener('click', closeModal);

        // Add escape key handler
        document.addEventListener('keydown', function escapeHandler(e) {
            if (e.key === 'Escape') {
                closeModal();
                document.removeEventListener('keydown', escapeHandler);
            }
        });
    })
    .catch(error => {
        // Remove loading modal if it exists
        if (loadingModal.parentNode) {
            document.body.removeChild(loadingModal);
        }
        console.error('Error describing column:', error);
        alert(error.message || 'Error describing column');
    });
}

function deleteColumn(columnName) {
    // ask to delete the column
    const confirmDelete = confirm(`Are you sure you want to delete column ${columnName}?`);
    if (!confirmDelete) return;

    const data = {
        columnName: columnName,
        action: 'delete'
    };

    fetch('http://localhost:5000/analysis/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        displayData(result);
        updateMetrics(result);
    })
    .catch(error => {
        console.error('Error deleting column:', error);
        alert('Error deleting column: ' + error.message);
    });
}

async function filterColumn(columnName) {
    try {
        const filterValue = prompt(`Enter filter value for ${columnName}:`);
        if (filterValue === null || filterValue.trim() === '') {
            return; // User cancelled or entered empty value
        }

        // Convert to number if the input is numeric
        const parsedValue = !isNaN(filterValue) ? Number(filterValue) : filterValue;

        const data = {
            columnName: columnName,
            filterValue: parsedValue
        };
        const response = await fetch('http://localhost:5000/analysis/filter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Filter failed with status: ${response.status}`);
        }

        const result = await response.json();

        if (!result.data || !result.columns) {
            throw new Error('Invalid response format from server');
        }

        displayData(result);
        updateMetrics(result);
    } catch (error) {
        alert(`Error filtering data: ${error.message}`);
    }
}

// Execute Python code
document.getElementById('executePython').addEventListener('click', async () => {
    if (!window.pythonEditor) {
        console.error('Python editor not initialized');
        alert('Python editor not initialized. Please refresh the page.');
        return;
    }

    if (!window.currentData) {
        console.error('No data available');
        alert('Please upload a data file first.');
        return;
    }

    try {
        const code = window.pythonEditor.getValue();
        
        const response = await fetch('http://localhost:5000/execute-python', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code: code,
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to execute Python code');
        }

        const result = await response.json();
        
        // Save the new data
        localStorage.setItem('currentData', JSON.stringify(result));
        displayData(result);
    } catch (error) {
        console.error('Error executing Python code:', error);
        alert('Error executing Python code: ' + error.message);
    }
});

// Reset data to original state
document.getElementById('resetData').addEventListener('click', () => {
    try {
        const originalData = localStorage.getItem('originalData');
        if (originalData) {
            const data = JSON.parse(originalData);
            
            // Update window variables
            window.currentData = data;
            window.originalData = data;
            
            // Update localStorage
            localStorage.setItem('currentData', originalData);
            
            // Redisplay the data
            displayData(data);
            
            // Reset the Python editor content
            if (window.pythonEditor) {
                window.pythonEditor.setValue(`# Your Python code here
# The data is available as a pandas DataFrame in the 'df' variable
# Store your result in the 'result' variable

# Example: Filter data where column value is greater than 100
# df = df[df['column_name'] > 100]

# Example: Group by and calculate mean
# result = df.groupby('category')['value'].mean()

# Example: Sort data
# result = df.sort_values('column_name', ascending=False)

# Return the modified DataFrame
result = df
`);
            }
        } else {
            console.error('No original data found in localStorage');
            alert('No original data found. Please upload a data file first.');
        }
    } catch (error) {
        console.error('Error resetting data:', error);
        alert('Error resetting data: ' + error.message);
    }
}); 