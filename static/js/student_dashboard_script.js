
document.getElementById("addBtn").addEventListener("click", function () {
    document.getElementById("addclassform").classList.toggle("hidden");
});
document.getElementById("cross").addEventListener("click", function () {
    document.getElementById("addclassform").classList.add("hidden");
});
document.getElementById("cancel").addEventListener("click", function () {
    document.getElementById("addclassform").classList.add("hidden");
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('addClassForm').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        // Get form data
        var formData = new FormData(this);

        // Send POST request to backend
        fetch('/add_course', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'course_found') {
                    alert('Course ' + data.course + ' added successfully!');
                    // Clear input fields
                    document.getElementById('course_name').value = '';
                    document.getElementById('course_id').value = '';
                    document.getElementById('group_id').value = '';
                    window.location.reload();
                } else if (data.status === 'course_details_mismatch' || data.status === 'course_not_found') {
                    alert('Course ' + data.course + ' not found!');
                } else {
                    alert('Error: ' + data); // Show any other response from the backend
                }
            })
            .catch(error => {
                alert('Error: ' + error); // Show error if fetch request fails
            });
    });

    // Cancel button event handler
    document.getElementById('cancel').addEventListener('click', function () {
        document.getElementById('course_name').value = '';
        document.getElementById('course_id').value = '';
        document.getElementById('group_id').value = '';
    });
});





// function fetchStudyMaterials() {
//     // Make an AJAX request to the server to fetch study materials
//     fetch('/study-materials')
//         .then(response => response.json())
//         .catch(error => {
//             console.error('Error fetching study materials:', error);
//         });
// }


function uploadFile() {
    fetch('/upload', {
        method: 'POST'
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to upload file');
            }
            return response.json();
        })
        .then(data => {
            if (data.file_name === "course not selected") {
                alert("Please select course");
            } else {
                alert(`${data.file_name} uploaded successfully!`);
                window.location.reload();
                // console.log('File ID:', data.file_id);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to upload file');
        });
}
