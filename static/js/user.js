let formAddMember = document?.querySelector("#formAddMember")
let btnEditUser = document?.querySelector("#btnEditUser")
let btnEditUserSave = document?.querySelector("#btnEditUserSave")
let btnQuite = document?.querySelector("#btnQuite")
let divGenre = document?.querySelector('.divGenre')

formAddMember && formAddMember.addEventListener('submit', async(e) => {
    e.preventDefault()

    let fname = e.target['fname'].value.trim()
    let lname = e.target['lname'].value.trim()
    let lien = e.target['lien'].value.trim()

    if (fname && lname && lien){
        let response = await fetch('http://localhost:5000/api/member/',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({fname, lname, lien})
        })

        let data = await response.json()
        console.log(data)

        e.target['fname'].value = ""
        e.target['lname'].value = ""
        e.target['lien'].value = ""
    }

    e.target.parentElement.classList.remove('show')

})

btnEditUser && btnEditUser.addEventListener('click', () => {
    btnEditUserSave.style.display = "block"
    btnQuite.style.display = "block"
    btnEditUser.style.display = "none"
    divGenre.style.display = "flex"
    divGenre.style.flexDirection = "column"


    document.querySelectorAll('input').forEach( input => input.removeAttribute('disabled'))
})


btnQuite && btnQuite.addEventListener('click', () => {
    btnEditUserSave.style.display = "none"
    btnQuite.style.display = "none"
    divGenre.style.display = "none"
    btnEditUser.style.display = "block"

    document.querySelectorAll('input').forEach( input => input.setAttribute('disabled', 'true'))

})


