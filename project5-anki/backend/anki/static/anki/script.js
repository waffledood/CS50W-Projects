document.addEventListener("DOMContentLoaded", function () {
  // add Bootstrap form validation functionality to createCollectionForm
  const createCollectionForm = document.querySelector("#createCollectionForm");
  createCollectionForm.addEventListener(
    "submit",
    formValidationOnSubmit(createCollectionForm),
    false
  );
});

function formValidationOnSubmit(form) {
  return (event) => {
    // log function call
    console.log(`${form.id} form was submitted`);

    // check validity of form
    if (!form.checkValidity()) {
      event.preventDefault();
      event.stopPropagation();
    }

    // add was-validated class to form
    form.classList.add("was-validated");
  };
}
