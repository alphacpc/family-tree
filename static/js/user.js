let formAddMember = document.querySelector("#formAddMember")

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
