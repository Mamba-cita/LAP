console.log('Mamba-cita');

//check if the user exits

const checkIfUserExists = (event) => {
        const emailFormElement = event.target
        const email = event.target.value
        axios.post('/validate_user', {
            email: email

        })
         .then((response) => {
            if (response.data.exists) {
                emailFormElement.setCustomValidity('Email already exists,proceed to login')
                emailFormElement.reportValidity()
            } (error) => {
                console.log(error)
            }
        })
    }
      
