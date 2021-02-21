export const price = function(amount, format='USD') {
    let formatter;
    if(format.toUpperCase() == 'EUR') {
        formatter = new Intl.NumberFormat('nl-NL', {
            style: 'currency',
            currency: 'EUR'
        })
    }
    else if (format.toUpperCase() == 'USD') {
        formatter = new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'USD'
        })
    }
    if(!isNaN(amount)) {
        return formatter.format(amount);
    } else { return formatter.format(0); }
}