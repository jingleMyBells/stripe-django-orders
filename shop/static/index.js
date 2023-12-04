let key = document.querySelector("#pk_test")
let stripe = Stripe(key.textContent);
let buttons = document.querySelectorAll("button");
console.log(buttons.length);

for(var i = 0; i < buttons.length; i++) {
    let button = buttons[i]
    let button_id = button.id
    button.addEventListener("click", function(){
    fetch(`/buy/${button_id}/`, {
      method: 'GET',
    })
    .then(function(response) {
      return response.json();
    })
    .then(function(session) {
    console.log(session)
      return stripe.redirectToCheckout({ sessionId: session.id });
    })
    .then(function(result) {
      if (result.error) {
        alert(result.error.message);
      }
    });
    }, false);
}
