// ////////////////////////////////////
// //////// LES VARIABLES ////////////
// //////////////////////////////////

let btnShowForm = document?.querySelector('#btnShowForm')
let btnHideForm = document?.querySelector('.btnQuit')
let divOverlay =  document?.querySelector('.divOverlay')
let formOverlay = document?.querySelector('.divOverlay form')


// ///////////////////////////////////////////
// //////// LES ADDEVENTLISTENER ////////////
// /////////////////////////////////////////

btnShowForm && btnShowForm.addEventListener('click', () => {
    divOverlay.classList.add('show')
})

btnHideForm && btnHideForm.addEventListener('click', () => {
    formOverlay.preventDefault()
    divOverlay.classList.remove('show')
})

