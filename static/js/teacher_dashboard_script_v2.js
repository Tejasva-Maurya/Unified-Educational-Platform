document.getElementById("addBtn").addEventListener("click", function () {
    document.getElementById("createCourse").classList.toggle("hidden");
});
// Add event listener for hiding the create course form
document.getElementById("cross").addEventListener("click", function () {
    document.getElementById("createCourse").classList.add("hidden");
});

document.addEventListener('DOMContentLoaded', function () {
    // Add event listener for form submission
    document.getElementById('createCourseForm').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        // Get form data
        var formData = new FormData(this);

        // Send POST request to backend
        fetch('/create_course', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'course_created') {
                    alert('Course ' + data.course + ' created successfully!');
                    // Clear input fields
                    document.getElementById('course_name').value = '';
                    document.getElementById('course_id').value = '';
                    document.getElementById('group_id').value = '';
                    window.location.reload();
                } else if (data.status === 'Course_already_exists') {
                    alert('Course ' + data.course + ' already exists!');
                } else {
                    alert('Error: ' + data); // Show any other response from the backend
                }
            })
            .catch(error => {
                alert('Error: ' + error); // Show error if fetch request fails
            });
    });

    // Add event listener for cancel button
    document.getElementById('cancel').addEventListener('click', function () {
        // Clear input fields
        document.getElementById('course_name').value = '';
        document.getElementById('course_id').value = '';
        document.getElementById('group_id').value = '';
        // Hide the create course form
        document.getElementById("createCourse").classList.add("hidden");
    });
});

// Function to upload a file
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
