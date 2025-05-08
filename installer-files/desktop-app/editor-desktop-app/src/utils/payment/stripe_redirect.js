import { openUrl } from '@tauri-apps/plugin-opener';

async function redirectToStripeCheckout(email) {

  // Note, this is a development url, in the future, we need an actual domain url 
  try {
    const res = await fetch('http://127.0.0.1:8000/api/billing/create-session/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email: email })
    });
  
    // Check if the response status is OK (200)
    if (!res.ok) {
      console.error('Error: Response not OK', res.status, res.statusText);
      const errorData = await res.json();
      console.error('Error response from backend:', errorData);
      return;
    }
    
    const data = await res.json();
  
    if (data.session_url) {
      // Open in default browser (not inside app)
      console.log("opening checkout")
      await openUrl(data.session_url);
      return data.session_id
    } else {
      console.error('No session URL returned');
    }
  } catch (err) {
    console.error('Failed to redirect to Stripe Checkout:', err);
  }
}

export default redirectToStripeCheckout;


// See if we success redirect to a checkout url when this function runs. 
// Note, the django backend needs to be running to serve 