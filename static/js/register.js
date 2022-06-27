let formRegister = document?.querySelector(".divRegister form")
let divMessageError = document?.querySelector(".divMessageError")


let funcShowMessage = (message) => {
    let p = document.createElement('p')
    p.innerText = message
    divMessageError.append(p)
    divMessageError.classList.add('show')

    setTimeout(() => {
        console.log("first")
        p.innerText = ''
        p.remove()
        divMessageError.classList.remove('show')

    }, 3000)
}



formRegister.addEventListener('submit', async(e) => {
    e.preventDefault()

    let fname = e.target['fname'].value.trim()
    let lname = e.target['lname'].value.trim()
    let email = e.target['email'].value.trim()
    let mdp = e.target['mdp'].value.trim()
    let mdpc = e.target['mdpc'].value.trim()

    if( fname == "" || lname == "" || email == "" || mdp == "" || mdpc == ""){
        funcShowMessage("Veillez remplir tous les champs")
    }
    else if (mdp.length < 2){
        funcShowMessage("Veillez donner un mot de passe contenant au moins 8 caractères !")
    }
    else if( mdp != mdpc){
        funcShowMessage("Les deux mots de passe ne sont pas identiques !")
    }
    else{

        let response = await fetch('http://localhost:5000/api/register/',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({fname, lname, email, mdp})
        })

        // Récupper les données de l'APIs
        let data = await response.json()

        if(!data['type']) funcShowMessage(data['message'])
        
        
    }

})


