document.addEventListener("DOMContentLoaded", () => {
    window.DialogModal = function (DialogName, DialogButtonOpen, DialogButtonClose, DialogClassVisible) {
        let Dialog = document.querySelector(DialogName)
        let ButtonOpen = document.querySelector(DialogButtonOpen)
        let ButtonClose = document.querySelector(DialogButtonClose)


        ButtonOpen.addEventListener("click", () => {
            Dialog.classList.add(DialogClassVisible);
            document.body.style.overflowY = "hidden"
        })

        ButtonClose.addEventListener("click", () => {
            Dialog.classList.remove(DialogClassVisible);
            document.body.style.overflowY = "visible"
        })
    }
})