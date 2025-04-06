document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediction-form');
    const analysisComplete = document.getElementById('analysis-complete');
    const predictionResult = document.getElementById('prediction-result');
    
    // Check if we have a prediction result
    if (predictionResult.textContent.trim() !== '') {
        predictionResult.style.display = 'block';
        
        // Update stats with some sample values if prediction exists
        document.getElementById('followers-stat').textContent = '1.0K';
        document.getElementById('engagement-stat').textContent = '11.00%';
        document.getElementById('avg-time-stat').textContent = '0.2h';
    }
    
    // Handle form submission
    if (form) {
        form.addEventListener('submit', function(e) {
            // Show loading animation
            e.preventDefault();
            
            // Show the analysis complete screen
            analysisComplete.style.display = 'flex';
            
            // After a delay, submit the form
            setTimeout(() => {
                form.submit();
            }, 2000);
        });
    }
    
    // Fill form with values if they exist in URL params
    const urlParams = new URLSearchParams(window.location.search);
    const formFields = [
        'follower_count', 
        'hashtags_count', 
        'post_type', 
        'time_of_day', 
        'caption_length', 
        'avg_likes', 
        'avg_comments'
    ];
    
    formFields.forEach(field => {
        if (urlParams.has(field)) {
            const element = document.getElementById(field);
            if (element) {
                element.value = urlParams.get(field);
            }
        }
    });
});