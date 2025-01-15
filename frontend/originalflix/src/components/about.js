function About() {
    return(
        <section id="About" className="leading-7">
            <h3 className="text-2xl font-bold my-4">What is it?</h3>
            <p className="mb-4">
                <em>Ever needed to determine whether a piece of content is a streaming platform original for your app? You've come to the right place.</em>
            </p>
            <p>
                The OriginalFlix API allows developers to access a database of all originally produced or exclusive content for streaming platforms like Netflix, Hulu, and Amazon Prime Video. You can use this API to access and retrieve a robust catalog of original movies and shows categorized by streaming services, genres, and more.
            </p>

            <h3 className="text-2xl font-bold my-4">Features</h3>
            <ul>
                <li><strong>→ Advanced Filtering:</strong> Easy filtering and searching capabilities across multiple columns of the database.</li>
                <li><strong>→ No Authentication Required:</strong> Free and accessible via GET requests for all users</li>
                <li><strong>→ Unlimited Calls:</strong> There is no ceiling on the amount of calls that can be made</li>
            </ul>

            <h3 className="text-2xl font-bold my-4">How does it work?</h3>
            <ul className="mb-4">
                <li><strong>→ Backend:</strong> The database is compiled by scraping relevant Wikipedia articles using BeautifulSoup4 for details on originally produced or exclusively distributed content by streaming services. FastAPI is used to create the endpoints to ensure deployment efficiency.</li>
                <li><strong>→ Database:</strong> SQLAlchemy is used with PostgreSQL for seamlesss data management.</li>
                <li><strong>→ Deployment:</strong> The data is cleaned and stored in an Azure flexible PostgreSQL server. This React webpage is deployed using Vercel, and the API endpoints are deployed using Heroku to ensure scalability and reliability.</li>
            </ul>
            <p className="mb-4">
                The database will be updated periodically, and code will be updated to include newly made Wikipedia pages, such as the yearly cataogs of Netflix original movies. All updates can be found in the <a href="#Changelog" className="font-bold hover:underline">Changelog</a>.
            </p>
            <p>
                A huge thanks to <a className="font-bold hover:underline" href="https://www.lineate.design/" target="_blank" rel="noreferrer">Lineate Designs</a> for helping bring this website to life.
            </p>
            
            <h3 className="text-2xl font-bold my-4">Built with OriginalFlix</h3>
            <p>
                The <a className="font-bold hover:underline" href="https://chromewebstore.google.com/detail/custom-tudum/plkcjhmgcploglmdgbalngcnjholcamm">Custom Tudum Chrome extension</a> integrates the OriginalFlix API to allow users to replace the Tudum sound that plays at the beginning of all Netflix Originals.
            </p>
        </section>
    );
}

export default About