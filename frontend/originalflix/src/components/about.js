function About() {
    return(
        <section id="About">
            <h3>What is it?</h3>
            <p>
                The OriginalFlix API allows developers to quickly access a database of originally produced or exclusive content for streaming platforms like Netflix and Amazon Prime Video. Built for efficiency and simplicity, you can use this API to access and retrieve a robust catalog of original movies and shows categorized by streaming services, genres, and more. Ever needed to determine whether a piece of content is a streaming platform original for your program? You've come to the right place.
            </p>

            <h3>Features</h3>
            <ul>
                <li>Advanced Filtering: With endpoints tailored for flexibility, the API supports easy filtering and searching capabilities across multiple columns of the database.</li>
                <li>No Authentication Required: The API is free and accessible via GET requests for all users.</li>
                <li>Unlimited Calls: There is no ceiling on the amount of calls that can be made to the API.</li>
            </ul>

            <h3>How does it work?</h3>
            <p>
                Backend: The database is compiled by scraping relevant Wikipedia (using BeautifulSoup4) articles for details on originally produced or exclusively distributed content by streaming services. FastAPI was used to create the endpoints to ensure deployment efficiency.
                Database: SQLAlchemy was used with PostgreSQL for seamlesss data management.
                Deployment: The data is cleaned and stored in an Azure flexible server. This React webpage is deployed using Vercel, and the API endpoints are deployed using Heroku to ensure scalability and reliability.
            </p>
            <p>
                The database will be updated periodically, and code will be updated to include newly made Wikipedia pages, such as the yearly cataogs of Netflix original movies. All updates can be found in the Changelog.
            </p>
            <h3>Check out this Implementation!</h3>
            <p>
                The project that led to the creation of this API, is the first live integration of the API in an application. The Custom Tudum Chrome extension uses the OriginalFlix API to allow users to replace the Tudum sound that plays at the beginning of all Netflix Originals. Check it out in the Chrome Webstore today!
            </p>
            <h3>Logo and UI Design</h3>
            <p>
                A huge thank you to Rudra Sharma from Lineate Designs for helping bring this website to life.
            </p>
        </section>
    );
}

export default About