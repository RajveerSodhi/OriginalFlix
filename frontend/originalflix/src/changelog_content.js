const changelogContent = [
    {
        date: "Mar 4, 2025",
        content: [
            "The datebase has been updated; Netflix Original movies from 2020 - 2022 have been added. 2023 data and Zee5's original movie library still missing.",
        ]
    },
    {
        date: "Mar 1, 2025",
        content: [
            "Switched backend from Heroku to Render (free tier), causing a large delay in getting the API callback after periods of inactivity.",
        ]
    },
    {
        date: "Jan 13, 2025",
        content: [
            "Future updates will try to patch the columns of the database without valid values by implementing scraping code specific to each Wikipedia page format.",
            "The datebase has been refreshed with an added source_id column fo tracking information validity from the source.",
            "Improved the API endpoint responses to include more information."
        ]
    },
    {
        date: "Jan 8, 2025",
        content: [
            "Due to backend errors, data for Netflix Original movies from 2020-2023 and all of Zee5's original movie catalog is not included as of now.",
            "OriginalFlix API v1 deployed."
        ]
    },
]

export default changelogContent