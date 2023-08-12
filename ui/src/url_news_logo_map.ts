// Description: Map of news logo to url
const map_url_logo = {
    "abcnews" : "abc.png",
    "abcnews.go" : "abc.png",
    "apnews" : "apnews.png",
    "bbc" : "bbc.png",
    "breitbart" : "breitbart.png",
    "cbsnews" : "cbs.png",
    "cnbc" : "cnbc.png",
    "cnet" : "cnet.png",
    "cnn" : "cnn.png",
    "foxbusiness" : "foxbusiness.png",
    "foxnews": "foxnews.png",
    "guardian" : "guardian.png",
    "latimes" : "latimes.png",
    "motherjones" : "motherjones.png",
    "msnbc" : "msnbc.png",
    "nature" : "nature.png",
    "nbcnews" : "nbc.png",
    "newscientist" : "newscientist.png",
    "nytimes" : "nytimes.png",
    "politico" : "politico.png",
    "reuters" : "reuters.png",
    "news.sky" : "sky.png",
    "theguardian" : "theguardian.png",
    "thehill" : "thehill.png",
    "tomshardware" : "tomshardware.png",
    "usatoday" : "usatoday.png",
    "vox" : "vox.png",
    "washingtonpost" : "washingtonpost.png"
}

// Description: Map of news name to url
const map_url_name = {
    "abcnews" : "ABC",
    "abcnews.go" : "ABC",
    "apnews" : "AP",
    "bbc" : "BBC",
    "breitbart" : "Breitbart",
    "cbsnews" : "CBS",
    "cnbc" : "CNBC",
    "cnet" : "CNET",
    "cnn" : "CNN",
    "foxbusiness" : "FOX Business",
    "foxnews": "FOX",
    "guardian" : "Guardian",
    "latimes" : "LAT",
    "motherjones" : "Mother Jones",
    "msnbc" : "MSNBC",
    "nature" : "Nature",
    "nbcnews" : "NBC",
    "newscientist" : "New Scientist",
    "nytimes" : "NYT",
    "politico" : "Politico",
    "reuters" : "Reuters",
    "news.sky" : "Sky",
    "theguardian" : "Guardian",
    "thehill" : "The Hill",
    "tomshardware" : "Tom's Hardware",
    "usatoday" : "USA Today",
    "vox" : "Vox",
    "washingtonpost" : "Wapo"
}

// Description: Map url to logo file name
export function url2logo(url: string): string {
    const domain = (new URL(url)).hostname.replace('www.','');
    const short_domain = domain.replace('.com','');
    // @ts-ignore
    return map_url_logo[short_domain];
}

export function url2name(url: string): string {
    const domain = (new URL(url)).hostname.replace('www.','');
    const short_domain = domain.replace('.com','');
    // @ts-ignore
    return map_url_name[short_domain];
}

export const TOPICS_IMAGES = {
    "Biden's Student Loan Forgiveness": "https://media.cnn.com/api/v1/images/stellar/prod/230807142555-biden-student-loan-legal-challenges.jpg?c=16x9&q=h_720,w_1280,c_fill/f_webp",
    "DeSantis Suspends Prosecutor": "https://www.motherjones.com/wp-content/uploads/2023/08/DeSantisWorrell080923.jpg?resize=1536,863",
    "Ghost Guns": "https://media.cnn.com/api/v1/images/stellar/prod/230728181332-ghost-guns-dc-metro-police-file.jpg?c=original",
    "Hawaii Wild Fires - Aug 11, 2023": "https://i.guim.co.uk/img/media/24f75cc3a73679d1dded8b752f0620e60ee9f483/0_117_5670_3403/master/5670.jpg?width=700&dpr=2&s=none",
    "Hawaii Wild Fires - Aug 9, 2023": "https://image.cnbcfm.com/api/v1/image/107283956-16915943742023-08-09t151315z_1929337192_rc27k2al82wp_rtrmadp_0_hawaii-wildfire.jpeg?v=1691596838&w=740&h=416&ffmt=webp&vtcrop=y",
    "LK-99 Superconductor": "https://cdn.mos.cms.futurecdn.net/b73KVuHeQNVQJpQotbJRGH-1920-80.jpg.webp",
    "Ohio Vote on Constitutional Amendment": "https://www.politico.com/dims4/default/d103112/2147483647/strip/true/crop/3000x2000+0+0/resize/1260x840!/quality/90/?url=https%3A%2F%2Fstatic.politico.com%2F8d%2F0b%2Fdc70775c4d4f92363b224642e275%2F230808-ohio-vote-ap-2.jpg",
    "Trump Twitter Search Warrant": "https://dims.apnews.com/dims4/default/2fbfd98/2147483647/strip/true/crop/4911x3274+0+0/resize/1440x960!/format/webp/quality/90/?url=https%3A%2F%2Fassets.apnews.com%2F8f%2F17%2Ff643ab9563b2dd6a4de2cf6aacd0%2Fcf3c9e7fb9df4f6c9d1c98f833c06051",
}
