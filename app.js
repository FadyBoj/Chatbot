 
const option = {
    method:'POST',
    headers:{
        'Content-Type':'application/json'
    },
    body:JSON.stringify({
        email:"Fadynabil701@gmail.com",
        password:"123456789"
    })
}

const getData = async() =>{
    const response = await fetch('https://xfood.onrender.com/check-auth')
    const data = await response.json();
    console.log(data);
}

const login = async() =>{
    try {
        
        const response = await fetch('https://xfood.onrender.com/login',option)
        const data = await response.json();
        console.log(data)
    } catch (error) {
        console.log(error)
    }
}

login()