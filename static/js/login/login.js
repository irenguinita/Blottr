// Login feature JS. Currently just a placeholder hook — kept in its own
// feature folder per the vertical slicing rule, ready to extend later
// (e.g. client-side validation) without touching other features.
document.addEventListener("DOMContentLoaded", function () {
    const usernameField = document.getElementById("username");
    if (usernameField) {
        usernameField.focus();
    }
});
