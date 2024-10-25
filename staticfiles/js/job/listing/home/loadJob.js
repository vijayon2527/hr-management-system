// Utility function for AJAX requests
function fetchData(url, callback) {
    fetch(url, {
        method: 'GET',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => callback(data))
    .catch(error => console.error('Error fetching data:', error));
}

// Load more jobs
document.addEventListener('DOMContentLoaded', function () {
    const loadMoreBtn = document.getElementById('load-more-btn');
    loadMoreBtn?.addEventListener('click', function () {
        const page = this.getAttribute('data-page');
        loadMoreJobs(page);
    });

    function loadMoreJobs(page) {
        const url = `?page=${page}`;
        fetchData(url, function (data) {
            const jobList = document.getElementById('job-list');
            jobList.innerHTML += data.jobs_html;

            if (data.has_next) {
                loadMoreBtn.setAttribute('data-page', parseInt(page) + 1);
            } else {
                loadMoreBtn.remove();
            }
        });
    }
});

// Load job details into job detail section or modal
function loadJobDetails(slug, displayInModal = false) {
    const url = `?job_title=${slug}`;
    fetchData(url, function (data) {
        if (displayInModal) {
            showModal(data.job_detail_html);
        } else {
            const jobDetailContainer = document.querySelector('.job-detail .sticky-detail');
            jobDetailContainer.innerHTML = data.job_detail_html;
        }
    });
}

// Show job details in a modal using Bootbox
function showModal(content) {
    bootbox.dialog({
        title: "Job Details",
        message: content,
    });
}
