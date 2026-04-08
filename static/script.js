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
    fetch('/products/total_products')
        .then(res => res.json())
        .then(data => {
            document.getElementById('totalProducts').textContent = data.toLocaleString();
        }).catch(err => console.error('Error loading total products:', err));

}

function loadAverageRating() {
    fetch('/products/avg_rating')
        .then(res => res.json())
        .then(data => {
            document.getElementById('averageRating').textContent = data.toFixed(2);
        }).catch(err => console.error('Error loading average rating:', err));
}

function loadTotalDiscountedProducts() {
    fetch('/products/total_discounted')
        .then(res => res.json())
        .then(data => {
            document.getElementById('discountedProducts').textContent = data.toLocaleString();
        }).catch(err => console.error('Error loading total discounted products:', err));
}

function loadTotalReviews() {
    fetch('/products/total_reviews')
        .then(res => res.json())
        .then(data => {
            document.getElementById('totalReviews').textContent = data.toLocaleString();
        }).catch(err => console.error('Error loading total reviews:', err));
}


function loadTopRated() {
    fetch('/products/top-rated?min_reviews=50&limit=5')
        .then(res => res.json())
        .then(data => {
            const ratings = data.map(p => p.rating);

            new Chart(document.getElementById('topRatedChart'), {
                type: 'bar',
                data: {
                    labels: data.map(p => p.product_name.length > 100 ? p.product_name.substring(0,100) + '...' : p.product_name),
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
                const reviewCounts = data.map(p => p.rating_count);
                new Chart(document.getElementById('mostReviewedChart'), {
                    type: 'bar',
                    data: {
                        labels: data.map(p => p.product_name.length > 100 ? p.product_name.substring(0,100) + '...' : p.product_name),
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
            const discounts = data.map(p => p.discount_percentage);
            new Chart(document.getElementById('discountedChart'), {
                type: 'bar',
                data: {
                    labels: data.map(p => p.product_name.length > 100 ? p.product_name.substring(0,100) + '...' : p.product_name),
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

        fetch(`/products/filter?${category}&min_price=${minPrice}&max_price=${maxPrice}&min_rating=${minRating}&limit=10`)
            .then(res => res.json())
            .then(data => {
                const tbody = document.getElementById('filteredProductsTable');
                tbody.innerHTML = `<thead>
                    <tr>
                        <th>Product Name</th>
                        <th>Price</th>
                        <th>Rating</th>
                    </tr>
                </thead>`;
                data.forEach(p => {
                    const row = `<tr>
                        <td>${p.product_name}</td>
                        <td>$${p.actual_price.toFixed(2)}</td>
                        <td>${p.rating}</td>
                        </tr>`;
                    tbody.innerHTML += row;
                });
            }).catch(err => console.error('Error loading filtered products:', err));
        });
}