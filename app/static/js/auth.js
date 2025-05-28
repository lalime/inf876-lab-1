(function() {
    // your page initialization code here
    // the DOM will be available here
    console.log("Script chargé !");
    console.log("Script chargé 2!");

    document.getElementById('submit-form').addEventListener('click', async function (e) {
        e.preventDefault();
        const email = document.querySelector('[name="email"]').value;
        const password = document.querySelector('[name="password"]').value;
        console.log("Email:", email);
        try {
           
            const userCredential = await firebase.auth().signInWithEmailAndPassword(email, password);
            console.log("Utilisateur connecté :", userCredential.user);
            const idToken = await userCredential.user.getIdToken();
            document.querySelector('[name="idToken"]').value = idToken;

            console.log("Token d'identification :", idToken);
        } catch (error) {
            console.error('Erreur de connexion JS :', error);
            document.querySelector('[name="error"]').value = error.message;
            console.error('Erreur de connexion : ' + error.message);
        }
        
        document.getElementById('login-form').submit();

    });
 })();

