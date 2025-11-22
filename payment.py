const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

// Create a new customer
const createCustomer = async (email, metadata) => {
    return await stripe.customers.create({
        email,
        metadata,
    });
};

// Create a subscription
const createSubscription = async (customerId, priceId) => {
    return await stripe.subscriptions.create({
        customer: customerId,
        items: [{ price: priceId }],
    });
};

// Retrieve subscription status
const getSubscription = async (subscriptionId) => {
    return await stripe.subscriptions.retrieve(subscriptionId);
};

module.exports = {
    createCustomer,
    createSubscription,
    getSubscription,
};
