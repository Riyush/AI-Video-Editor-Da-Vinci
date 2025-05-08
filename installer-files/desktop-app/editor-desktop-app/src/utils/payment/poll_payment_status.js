// This function repeatedly polls the check-payment-status endpoint in django
// to see if payment has concoluded. Eventually polling returns True indicating
// sucessful completion of payment or false indicating failure

async function pollPaymentStatus(sessionId) {
    while (true) {
    console.log("checking payment completion")
    // will need to ensure localhost vs prodiction environment
      const res = await fetch('http://127.0.0.1:8000/api/billing/check-payment-status/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId })
      });
      const data = await res.json();
  
      if (data.payment_status === 'paid') {
        console.log("Payment complete!");
        // We navigate to the next page back in the submit form button
        return data.customer_id;
      }
      //create some behavior that occurs if the payment fails, maybe we get a response that says error?
      if (data.status === 'expired'){
        console.log("Session expired")
        // payment session concluded without payment, do an appropriate behaviors
        return null;
      }
      await new Promise(resolve => setTimeout(resolve, 5000)); // wait 5s before retry
    }
  }

export default pollPaymentStatus;