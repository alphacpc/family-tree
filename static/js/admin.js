let formAddUser = document.querySelector("#formAddUser")

formAddUser && formAddUser.addEventListener('submit', async(e) => {
    e.preventDefault()

    let fname = e.target['fname'].value.trim()
    let lname = e.target['lname'].value.trim()
    let email = e.target['email'].value.trim()
    let mdp = e.target['mdp'].value.trim()

    if (fname && lname && email && mdp){
        let response = await fetch('http://localhost:5000/api/user/',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({fname, lname, email, mdp})
        })

        let data = await response.json()
        console.log(data)

        e.target.parentElement.classList.remove('show')
        e.target['fname'].value = ""
        e.target['lname'].value = ""
        e.target['email'].value = ""
        e.target['mdp'].value = ""
    }
})

