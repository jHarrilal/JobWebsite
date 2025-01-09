document.addEventListener('DOMContentLoaded', function () {
    const listViewButton = document.getElementById('listViewButton');
    const gridViewButton = document.getElementById('gridViewButton');
    const jobListings = document.querySelector('.job_listings');

    // Set initial view mode from localStorage or fallback to 'list'
    const savedViewMode = localStorage.getItem('viewMode') || 'list';
    setViewMode(savedViewMode);

    // Event listeners for view mode buttons
    listViewButton.addEventListener('click', () => {
        setViewMode('list');
        saveViewMode('list');
    });

    gridViewButton.addEventListener('click', () => {
        setViewMode('grid');
        saveViewMode('grid');
    });

    // Function to set the view mode
    function setViewMode(mode) {
        if (mode === 'grid') {
            jobListings.classList.add('row', 'row-cols-1', 'row-cols-md-2', 'row-cols-lg-3', 'g-4');
            gridViewButton.classList.add('active');
            listViewButton.classList.remove('active');
        } else {
            jobListings.classList.remove('row', 'row-cols-1', 'row-cols-md-2', 'row-cols-lg-3', 'g-4');
            gridViewButton.classList.remove('active');
            listViewButton.classList.add('active');
        }
    }

    // Function to save view mode to localStorage
    function saveViewMode(mode) {
        localStorage.setItem('viewMode', mode);
    }
});
