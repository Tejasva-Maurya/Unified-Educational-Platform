document.addEventListener("DOMContentLoaded", function () {
    const classContainer = document.getElementById('classContainer');
    const cardContainer = document.getElementById('cardContainer');
    const containerMap = new Map(); // Map to store course ID and its associated card container

    function fetchCourseData() {
        fetch('/studentCourseData')
            .then(response => response.json())
            .then(courseDataList => {
                courseDataList.forEach(courseData => {
                    const courseId = courseData.course_id; // Preserve the original case of course_id
                    const groupId = courseData.group_id; // Preserve the original case of course_id

                    // Create card container for each course
                    const cardContainerForCourse = document.createElement('div');
                    cardContainerForCourse.id = `${courseId}CardContainer`;
                    cardContainerForCourse.classList.add('cardContainer');
                    cardContainerForCourse.classList.add("hidden");

                    containerMap.set(courseId, cardContainerForCourse);

                    // Create class card
                    const classCard = document.createElement('div');
                    classCard.classList.add("classCard");
                    classCard.innerHTML = `
                        <div class="classImg">
                            <img src="${BASE_URL}img/book.svg" alt="Book">
                        </div>
                        <div class="classInfo">
                            <h3>${courseData.course_name}</h3>
                            <h6>Course ID: ${courseId}</h6>
                            <h6>Group ID: ${groupId}</h6>
                        </div>
                    `;
                    classCard.dataset.courseId = courseId; // Set courseId as a data attribute
                    classCard.dataset.groupId = groupId; // Set courseId as a data attribute

                    classCard.addEventListener('click', function () {
                        const clickedCourseId = this.dataset.courseId; // Get courseId from data attribute
                        const clickedGroupId = this.dataset.groupId; // Get courseId from data attribute
                        // alert(clickedCourseId)
                        toggleClassContainer(clickedCourseId); // Toggle the visibility of class container
                        fetchFiles(clickedCourseId, clickedGroupId); // Fetch and display files for the clicked course
                    });

                    classContainer.appendChild(classCard);
                    cardContainer.appendChild(cardContainerForCourse); // Append the card container to the cardContainer div
                });
            })
            .catch(error => console.error('Error fetching course data:', error));
    }

    function fetchFiles(courseId, groupId) {
        fetch("/course_files", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ course_id: courseId, group_id: groupId }) // Send course_id to the backend
        })
            .then(response => response.json())
            .then(files => {
                const cardContainerForCourse = containerMap.get(courseId);
                cardContainerForCourse.innerHTML = ''; // Clear previous files
                files.forEach(file => {
                    const card = document.createElement('div');
                    card.classList.add('card');
                    card.innerHTML = `
                        <div class="fileicon">
                            <img src="${BASE_URL}img/pdficon.svg" alt="Assignment">
                        </div>
                        <div class="info">
                            <h3><a href="${file.link}">${file.name}</a></h3>
                            <p>${file.name}</p>
                        </div>
                    `;
                    cardContainerForCourse.appendChild(card);
                });
                cardContainerForCourse.classList.remove("hidden"); // Show the card container after files are added
            })
            .catch(error => console.error('Error fetching files:', error));
    }

    function toggleClassContainer(courseId) {
        containerMap.forEach((cardContainerForCourse, id) => {
            if (id === courseId) {
                if (cardContainerForCourse.classList.contains("hidden")) {
                    cardContainerForCourse.classList.remove("hidden");
                } else {
                    cardContainerForCourse.classList.add("hidden");
                }
            } else {
                cardContainerForCourse.classList.add("hidden");
            }
        });
    }

    // Initial fetch of course data
    fetchCourseData();
});
