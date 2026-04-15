document.addEventListener('DOMContentLoaded', () => {
    loadTotalProducts();
    loadAverageRating();
    loadTotalDiscountedProducts();
    loadTotalReviews();
    loadTopRated();
    loadMostReviewed();
    loadDiscounted();
    setupFilterForm();
    // You can also call other load functions here for discounted, most reviewed, etc.
});

function loadTotalProducts() {
    fetch('/products/total-products')
        .then(res => res.json())
        .then(data => {
            document.getElementById('totalProducts').textContent = data.total_products.toLocaleString();
        }).catch(err => console.error('Error loading total products:', err));

}

function loadAverageRating() {
    fetch('/products/avg-rating')
        .then(res => res.json())
        .then(data => {
            document.getElementById('averageRating').textContent = data.avg_rating.toFixed(2);
        }).catch(err => console.error('Error loading average rating:', err));
}

function loadTotalDiscountedProducts() {
    fetch('/products/total-discounted')
        .then(res => res.json())
        .then(data => {
            document.getElementById('discountedProducts').textContent = data.total_discounted.toLocaleString();
        }).catch(err => console.error('Error loading total discounted products:', err));
}

function loadTotalReviews() {
    fetch('/products/total-reviews')
        .then(res => res.json())
        .then(data => {
            document.getElementById('totalReviews').textContent = data.total_reviews.toLocaleString();
        }).catch(err => console.error('Error loading total reviews:', err));
}


function loadTopRated() {
    fetch('/products/top-rated?min_reviews=50&limit=5')
        .then(res => res.json())
        .then(data => {
            const ratings = data.top_rated.map(p => p.rating);

            new Chart(document.getElementById('topRatedChart'), {
                type: 'bar',
                data: {
                    labels: data.top_rated.map(p => p.product_name.length > 100 ? p.product_name.substring(0,100) + '...' : p.product_name),
                    datasets: [{
                    label: 'Rating',
                    data: ratings,
                    backgroundColor: '#007bff',
                    borderColor: '#000',
                    borderWidth: 1
                }]
            },
            options: {
                Responsesive: true,
                indexAxis: 'y',
                scales: {
                    x: {beginAtZero: true, max: 5}
                }
            }
        });
        }).catch(err => console.error('Error loading top rated products:', err));
}

function loadMostReviewed() {   
        fetch('/products/most-reviewed?limit=5')
            .then(res => res.json())
            .then(data => {
                const reviewCounts = data.most_reviewed.map(p => p.rating_count);
                new Chart(document.getElementById('mostReviewedChart'), {
                    type: 'bar',
                    data: {
                        labels: data.most_reviewed.map(p => p.product_name.length > 100 ? p.product_name.substring(0,100) + '...' : p.product_name),
                        datasets: [{
                            label: 'Number of Reviews',
                            data: reviewCounts,
                            backgroundColor: '#007bff',
                            borderColor: '#000',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        indexAxis: 'y',
                        scales: {
                            x: {beginAtZero: true, max: Math.max(...reviewCounts) + 10}  
                        }
                    }
                });
            }).catch(err => console.error('Error loading most reviewed products:', err));

}   

function loadDiscounted() {
    fetch('/products/discounted?limit=5')
        .then(res => res.json())
        .then(data => {
            const discounts = data.discounted.map(p => p.discount_percentage);
            new Chart(document.getElementById('discountedChart'), {
                type: 'bar',
                data: {
                    labels: data.discounted.map(p => p.product_name.length > 100 ? p.product_name.substring(0,100) + '...' : p.product_name),
                    datasets: [{
                        label: 'Discount Percentage',
                        data: discounts,
                        backgroundColor: '#007bff',
                        borderColor: '#000',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    indexAxis: 'y',
                    scales: {
                        x: {beginAtZero: true, max: 100}  
                    }
                }
            });
        }).catch(err => console.error('Error loading discounted products:', err));
}

function setupFilterForm() {
    const form = document.getElementById('filterForm');

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const category = document.getElementById('category').value;
        const minPrice = document.getElementById('minPrice').value;
        const maxPrice = document.getElementById('maxPrice').value;
        const minRating = document.getElementById('minRating').value;

        const url = `/products/filtered-products?category=${category}&min_price=${minPrice}&max_price=${maxPrice}&min_rating=${minRating}`;

        fetch(url)
            .then(res => res.json())
            .then(res => {
                const tbody = document.getElementById('filteredProductsBody');
                tbody.innerHTML = "";

                res.filtered_products.forEach(p => {
                    tbody.innerHTML += `
                        <tr>
                            <td>${p.product_name}</td>
                            <td>$${p.actual_price.toFixed(2)}</td>
                            <td>${p.rating}</td>
                        </tr>
                    `;
                });
            })
            .catch(err => console.error(err));
    });
}