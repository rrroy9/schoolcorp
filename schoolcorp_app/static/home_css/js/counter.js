    document.addEventListener('DOMContentLoaded', function() {
        const counters = document.querySelectorAll('.counter');
        const options = {
            threshold: 0.75, // Adjust the threshold as needed
        };

        const counterObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target;
                    const count = parseInt(target.innerText.replace(/\D/g, '')); // Extract digits from the count
                    let currentCount = 0;

                    // Set a fixed width to prevent layout shifts
                    target.style.width = target.offsetWidth + 'px';

                    const counterInterval = setInterval(() => {
                        target.innerText = currentCount.toLocaleString();
                        currentCount++;

                        if (currentCount > count) {
                            clearInterval(counterInterval);
                            observer.unobserve(target);
                        }
                    }, 10);
                }
            });
        }, options);

        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    });