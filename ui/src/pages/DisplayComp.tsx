import React, { useEffect, useState } from "react";
import FactsMap, { FactStruct, SourceStruct } from '../components/FactsMap';
import axios from "axios";
import { Typography, Box} from "@mui/material";
import Slider from '@mui/material/Slider';
import { url2logo, url2name } from '../url_news_logo_map';

const GET_TOPIC_URLS = 'https://just-the-facts.allen.ai/api/get-topic';
const COMPARE_FACTS = 'https://just-the-facts.allen.ai/api/compare-facts';

interface ServerFactStruct {
    fact: string;
    url: string;
    score: number;
}

const DisplayComp = () => {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const topic = urlParams.get('topic');
    let thresholdParam = Number(urlParams.get('threshold'));
    if (!thresholdParam) {
        thresholdParam = 0.9;
    }
    // @ts-ignore
    document.title = topic;
    const [sources, setSources] = useState<SourceStruct[]>([]);
    const [clusters, setClusters] = useState<FactStruct[][]>([]);
    const [threshold, setThreshold] = useState<number>(thresholdParam);
    const [pivotIdx, setPivotIdx] = useState<number>(0);
    useEffect(() => {
        axios.get(GET_TOPIC_URLS, { params: { topic: topic } }).then((res) => {
            console.log(res.data);
            const allSources = res.data.urls.reduce((acc: SourceStruct[], url: string) => {
                return [...acc, {url: url, logo: url2logo(url), name: url2name(url)}];
            }, []);
            console.log(allSources);
            setSources(allSources);
            // const allTopics = Object.keys(res.data).reduce((acc: TopicStruct[], topicName: string) => {
            //     return [...acc, { name: topicName, urls: res.data[topicName] }];

        });
    }, []);
    useEffect(() => {
        axios.get(COMPARE_FACTS, { params: { topic: topic, method: 'gpt-4', match_threshold: threshold } }).then((res) => {
            console.log(res.data);
            const topicClusters = res.data.map((cluster: ServerFactStruct[]) => {
                return cluster.map((fact: ServerFactStruct) => {
                    return { fact: fact.fact, url: fact.url, sourceName: url2name(fact.url) };
                });
            });
            console.log(topicClusters)
            setClusters(topicClusters);
        });
    }, []);

    const getOrderedUrls = (urls: string[], pivotIdx: number) => {
        const newUrls = [...urls];
        const tmpUrl = newUrls.splice(pivotIdx, 1);
        newUrls.unshift(tmpUrl[0]);
        return newUrls;
    }

    const setPivotArticle = (sourceIndex: number) => {
        const urlsByColumn = sources.map((source) => source.url);
        setPivotIdx(sourceIndex);
        const urls = getOrderedUrls(urlsByColumn, sourceIndex);
        axios.get(COMPARE_FACTS, {
            params: {
                method: 'gpt-4',
                match_threshold: threshold,
                urls: urls.join(','),
            }}
        ).then((res) => {
            console.log(res.data);
            const topicClusters = res.data.map((cluster: ServerFactStruct[]) => {
                return cluster.map((fact: ServerFactStruct) => {
                    return { fact: fact.fact, url: fact.url, sourceName: url2name(fact.url) };
                });
            });
            console.log(topicClusters)
            setClusters(topicClusters);
        });
    }

    const updateThreshold = (value: number | Array<number>) => {
        // @ts-ignore
        setThreshold(value);
        const urlsByColumn = sources.map((source) => source.url);
        const urls = getOrderedUrls(urlsByColumn, pivotIdx);
        axios.get(COMPARE_FACTS, {
            params: {
                method: 'gpt-4',
                match_threshold: value,
                urls: urls.join(','),
            }}
        ).then((res) => {
            console.log(res.data);
            const topicClusters = res.data.map((cluster: ServerFactStruct[]) => {
                return cluster.map((fact: ServerFactStruct) => {
                    return { fact: fact.fact, url: fact.url, sourceName: url2name(fact.url) };
                });
            });
            console.log(topicClusters)
            setClusters(topicClusters);
        });
    }

    return (
        <>
            <h3><a href="/">Just the Facts!</a> &gt; {topic}</h3>
            <Typography gutterBottom variant="body2">Cluster similarity threshold: {threshold} </Typography>
            <Box>

            <Slider

                aria-label="Temperature"
                value={threshold}
                valueLabelDisplay="auto"
                step={0.01}
                marks
                min={0.7}
                max={1}
                onChange={(event: React.SyntheticEvent | Event, value: number | Array<number>) => {
                    // console.log(value)
                    // @ts-ignore
                    setThreshold(value);
                }}
                onChangeCommitted={(event: React.SyntheticEvent | Event, value: number | Array<number>) => {
                    updateThreshold(value);
                }}
            />

            </Box>
            <FactsMap
                sources={sources}
                clusters={clusters}
                setPivotArticle={setPivotArticle}
                pivotIdx={pivotIdx}
            />
        </>
    )
}

export default DisplayComp;