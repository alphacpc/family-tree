let formAddUser = document.querySelector("#formAddUser")
let tbody = document.querySelector('tbody')


function funcGeneTr(uuid, fname, lname, email){
    
    if(document.querySelector('.no-users')){
        document.querySelector('.no-users').style.display = "None"
    }

    let tr = document.createElement('tr')
    let td_1 = document.createElement('td')
    let td_2 = document.createElement('td')
    let td_3 = document.createElement('td')
    let td_4 = document.createElement('td')
    let td_5 = document.createElement('td')

    td_1.innerText = uuid
    td_2.innerText = fname
    td_3.innerText = lname
    td_4.innerText = email
    td_5.innerHTML = `
        <a href="/detail?uuid=${uuid}" class="btn btn-more letter-spacing ft-15 pd-5 br-4">voir plus</a>
        <a href="/edit?uuid=${uuid}" class="btn btn-update letter-spacing ft-15 pd-5 br-4">Modifier</a>
        <a href="/archive?uuid=${uuid}" class="btn btn-archive letter-spacing ft-15 pd-5 br-4">Archiver</a>
    `

    tr.append(td_1)
    tr.append(td_2)
    tr.append(td_3)
    tr.append(td_4)
    tr.append(td_5)

    tbody.append(tr)
}



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
        const email_user = await data.data[0]['p.email']
        const lname_user = await data.data[0]['p.lname']
        const fname_user = await data.data[0]['p.name']
        const uuid_user = await data.data[0]['p.uuid']
    
        await funcGeneTr(uuid_user, fname_user, lname_user, email_user)

        e.target.parentElement.classList.remove('show')
        e.target['fname'].value = ""
        e.target['lname'].value = ""
        e.target['email'].value = ""
        e.target['mdp'].value = ""
    }
})

