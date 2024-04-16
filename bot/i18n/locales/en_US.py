from string import Template

en = {
    "Welcome": Template("Glad You are back, $name"),
    "email": Template("Email"),
    "ProvideYourEmail": Template("Provide your email"),
    "ChooseYourTimeZone": Template("Choose your time zone"),
    "UseOnlyLatinLetters": Template("Use only latin letters"),
    "ProvideYourFirstname": Template("Provide your first name"),
    "ProvideYourLastname": Template("Provide your last name"),
    "GreatWaitForConfirmationByAdmin": Template("Great! Wait for confirmation by Admin"),
    "OneMoreTime": Template("Try one more time"),
    "UseOnlyDigits": Template("Use only digits"),
    "SelectYourTimezone": Template("Select your timezone"),
    "SomethingWentWrong": Template("Something went wrong. Repeat registration process! Press /start"),
    "WelcomeOnBoard": Template("Welcome on board, You have successfully registered. Now You can choose what do You want to do!"),
    "SpecifyCourseCostPerHourInDollars": Template("Specify <b>$subject</b> course cost per hour in dollars"),
    "ChooseSubjectToTeach": Template("Choose subject to teach"),
    "UseOnlyNumbers": Template("Use only numbers"),
    "CourseAddedSuccessfully": Template("Course added successfully"),
    "SubscribeCourse": Template("Subject: $subject\nTutor: $tutor\nPrice: $price"),
    "NoCoursesFound": Template("No courses found"),
    "TutorInCourse": Template("Tutor: <b>$tutor</b>"),
    "StudentInCourse": Template("Student: <b>$student</b>"),
    "SubjectAndRoleInCourse": Template("Subject: $subject\n$role: $name"),
    "AdminPanelIsHere": Template("Admin panel is here"),
    "MainMenu": Template("Main menu"),
    "OfficeIsHere": Template("Office is here"),
    "NoAvailableSubjects": Template("No available subjects"),
    "YourClassroomIsHere": Template("Your classroom is here"),
    "ChooseSubject": Template("Choose subject"),
    "YouHaveNoCourses": Template("You have no courses"),
    "NoRequests": Template("No requests"),
    "AllRequests": Template("All requests"),
    "ChooseSubjectToLearn": Template("Choose subject to learn"),
    "YouHaveSuccessfullySubscribedToTheCourse": Template("You have successfully subscribed to the course"),
    "UsersRequestAccepted": Template("User\'s request accepted"),
    "UsersRequestDeclined": Template("User\'s request declined"),
    "CongratulationsYourRequestForRoleHasBeenAccepted": Template("Congratulations $name, Your request for $role role has been accepted"),
    "YouDontHaveClasses": Template("You dont have classes"),

    "TeachIKBtn": Template("Teach"),
    "StudyIKBtn": Template("Study"),
    "SubscribeIKBtn": Template("Subscribe"),
    "ReturnToSelectSubjectsIKBtn": Template("Return to select subjects"),
    "PlanClassIKBtn": Template("Plan class"),
    "AllClassesIKBtn": Template("All classes"),
    "AcceptIKBtn": Template("Accept"),
    "DeclineIKBtn": Template("Decline"),
    "BackIKBtn": Template("Back"),
    "BackToCourseIKBtn": Template("Back to course"),

    "ProfileKBtn": Template("Profile"),
    "SupportKBtn": Template("Support"),
    "OfficeKBtn": Template("Office"),
    "ClassroomKBtn": Template("Classroom"),
    "AdminPanelKBtn": Template("Admin panel"),
    "MyClassesKBtn": Template("My classes"),
    "SubscribeCourseKBtn": Template("Subscribe course"),
    "MainMenuKBtn": Template("Main menu"),
    "MyCoursesKBtn": Template("My courses"),
    "AddCourseKBtn": Template("Add course"),
    "TutorRequestsKBtn": Template("Tutor requests"),
    "StudentRequestsKBtn": Template("Student requests"),
}

