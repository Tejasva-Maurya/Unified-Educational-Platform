var loginUserType = "Student";
document.getElementById("studentButton").addEventListener("click", function () {
    loginUserType = "Student";
    document.getElementById("loginFields").innerHTML = `
        <label for="loginUserID">Roll No:</label>
        <input type="number" id="loginUserID" name="loginUserID" required>
        <label for="loginPassword">Password:</label>
        <input type="password" id="loginPassword" name="loginPassword" required>
    `;
    document.getElementById("loginForm").classList.toggle("hidden");
});
document.getElementById("teacherButton").addEventListener("click", function () {
    loginUserType = "Teacher";
    document.getElementById("loginFields").innerHTML = `
        <label for="loginUserID">Employee ID:</label>
        <input type="number" id="loginUserID" name="loginUserID" required>
        <label for="loginPassword">Password:</label>
        <input type="password" id="loginPassword" name="loginPassword" required>
    `;
    // document.getElementById("loginForm").style.display = "block";
    document.getElementById("loginForm").classList.toggle("hidden");
});

document
    .getElementById("registerStudentButton")
    .addEventListener("click", function () {
        userType = "Student";
        document.getElementById("registerFields").innerHTML = `
    <label for="name">Name:</label>
    <input type="text" id="name" name="name" required>
    <label for="userid">Roll No (ID):</label>
    <input type="number" id="userid" name="userid" required>
    <label for="gender">Gender:</label>
    <select id="gender" name="gender" required>
        <option value="male">Male</option>
        <option value="female">Female</option>
        <option value="other">Other</option>
    </select>
    <label for="semester">Semester:</label>
    <select id="semester" name="semester" required>
        <option value="1">1st semester</option>
        <option value="2">2nd semester</option>
        <option value="3">3rd semester</option>
        <option value="4">4th semester</option>
        <option value="5">5th semester</option>
        <option value="6">6th semester</option>
        <option value="7">7th semester</option>
        <option value="8">8th semester</option>
    </select>
    <label for="groupid">Group ID :</label>
    <input type="text" id="groupid" name="groupid" required>
    <label for="password">Password :</label>
    <input type="password" id="password" name="password" required>
    `;
        document.getElementById("registerForm").classList.toggle("hidden");
    });
document
    .getElementById("registerTeacherButton")
    .addEventListener("click", function () {
        userType = "Teacher";
        document.getElementById("registerFields").innerHTML = `
        <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
                <label for="userid">Empolyee ID:</label>
                <input type="number" id="userid" name="userid" required>
                <label for="gender">Gender:</label>
                <select id="gender" name="gender" required>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                </select>        
                <label for="password">Password :</label>
                <input type="password" id="password" name="password" required> 
    `;
        document.getElementById("registerForm").classList.toggle("hidden");
    });
function login() {
    var userid = document.getElementById("loginUserID").value;
    var password = document.getElementById("loginPassword").value;

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            userid: userid,
            password: password,
            loginUserType: loginUserType,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.message === "Login successful") {
                // Redirect to dashboard after successful login
                if (loginUserType === "Student") {
                    window.location.href = "/student/dashboard";
                } else {
                    window.location.href = "/teacher/dashboard";
                }
            } else {
                alert(data.message || data.error);
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}
function register() {
    var name = document.getElementById("name").value;
    var password = document.getElementById("password").value;
    var userid = document.getElementById("userid").value;
    var gender = document.getElementById("gender").value;
    if (userType == "Student") {
        var groupid = document.getElementById("groupid").value;
        var semester = document.getElementById("semester").value;
        fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: name,
                password: password,
                gender: gender,
                userid: userid,
                semester: semester,
                userType: userType,
                groupid: groupid,
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                alert(data.message || data.error);
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    } else {
        fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: name,
                password: password,
                gender: gender,
                userid: userid,
                userType: userType,
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                alert(data.message || data.error);
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    }
}
