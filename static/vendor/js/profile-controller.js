document.addEventListener("DOMContentLoaded", () => {
    let dropdownHead = document.querySelector("#dropdown-profile")
    let dropdonwContent = document.querySelector("#dropdown-profile-content")


    dropdownHead.addEventListener("click", () =>{
        dropdownHead.classList.toggle("dropdown-active")
        dropdonwContent.classList.toggle("dropdown__content--active");
    })

})