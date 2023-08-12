import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import styled from 'styled-components';
import useFetch, { CachePolicies } from 'use-http';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import {
    TextField,
    Select,
    Alert,
    AlertTitle,
    MenuItem,
    FormHelperText,
    Stack,
    InputLabel,
    FormControl,
    Typography,
    Box,
    Card,
    CardContent,
    CardActions,
    CardMedia,
    Avatar,
} from '@mui/material';
import Grid from '@mui/material/Grid';
import { LoadingButton } from '@mui/lab';
import { MaxWidthText } from '@allenai/varnish2/components';

import { Answer } from '../api/Answer';
import { Query } from '../api/Query';
import { error } from 'console';

import { TOPICS_IMAGES, url2logo } from '../url_news_logo_map';

/**
 * This type defines the different values that will be accepted from the form's inputs.
 * The names of the keys (Eg. 'question', 'choices') must match
 * the HTML input's declared 'name' attribute.
 *
 * Eg:
 * ``` <Form.Item label="Question:" name="question"> ... </Form.Item>
 *
 * In this example, we aligned the
 * form's 'name' attributes with the keys of the 'Query' type that is used to query the API.
 */
type FormValue = Partial<Query>;
interface FactStruct {
    text: string;
}

interface TopicStruct {
    name: string;
    urls: string[];
}

const TOPICS_URL = 'https://just-the-facts.allen.ai/api/list-topics';
export const Home = () => {
    const [articleUrl, setArticleUrl] = useState('');
    const [facts, setFacts] = useState<FactStruct[]>([]);
    const [topics, setTopics] = useState<TopicStruct[]>([]);

    useEffect(() => {
        axios.get(TOPICS_URL).then((res) => {
            const allTopics = Object.keys(res.data).reduce((acc: TopicStruct[], topicName: string) => {
                return [...acc, {name: topicName, urls: res.data[topicName]}];
            }, []);
            setTopics(allTopics);
        })
    }, []);

    const submitUrl = () => {
        axios.post(
            `/api/get-facts`,
            { url: articleUrl, }
        ).then((response) => {
            console.log(response.data)
            setFacts(response.data.facts);
        }).catch((error) => {
            console.log(error);
        });
    }

    return (
        <div>
            <h1>Just The Facts!</h1>

            <h2>Recent topics</h2>
            <Grid container spacing={2}>
            {
                topics.map((topic) => {
                    console.log(topic)
                    return (
                        <Grid item xs={3}>
                            <Card sx={{ minWidth: 275, height: '300px', cursor: 'pointer', '&:hover': { boxShadow: '0 0 11px rgba(33,33,33,.4)'  }}}
                                onClick={() => {
                                    // @ts-ignore
                                    window.location = `/components?topic=${topic.name}`;
                                }}
                            >
                                <CardMedia
                                    sx={{ height: 150 }}
                                    image={
                                        // @ts-ignore
                                        TOPICS_IMAGES[topic.name]
                                    }
                                    title="green iguana"
                                />
                                <CardContent sx={{ height: '60px', padding: '0px 10px'}} >
                                    <h5>{topic.name}</h5>
                                </CardContent>

                                <CardActions>
                                <Box>
                                    {// @ts-ignore
                                        topic.urls.urls.map((url) => {
                                        console.log(url)
                                        return (
                                            <Avatar
                                                src={`/${url2logo(url)}`}
                                                imgProps={{style: {objectFit: 'contain', background: 'white'}}}
                                                sx={{ width: 24, height: 24, fontSize: '10px', marginRight: '5px', display: 'inline-block' }}>1</Avatar>
                                        )
                                    })}
                                    </Box>
                                </CardActions>
                            </Card>
                        </Grid>
                    )
                })
            }
            </Grid>
            {/* <FormStack spacing={2}>
                <TextField
                    label="Article url"
                    name="article-url"
                    fullWidth
                    placeholder="Enter a url"
                    value={articleUrl}
                    onChange={(e) => setArticleUrl(e.target.value)}
                />
                <Button variant="contained"
                    onClick={submitUrl}>
                    Get facts!
                </Button>
            </FormStack>
            <div>
                <h3>Here are the facts:</h3>
                {facts.map((fact) => (
                    <Box sx={{padding: '4px 14px', borderBottom: '1px solid #eee'}}>
                        {fact.text}
                    </Box>
                ))}
            </div> */}
        </div>
    );
};

/**
 * The definition below creates a component that we can use in the render
 * function above that have extended / customized CSS attached to them.
 * Learn more about styled components:
 * @see https://www.styled-components.com/
 *
 *
 * CSS is used to modify the display of HTML elements. If you're not familiar
 * with it here's quick introduction:
 * @see https://developer.mozilla.org/en-US/docs/Web/CSS
 */
const FormStack = styled(Stack)`
    max-width: 600px;
`;

/**
 * Matches style for helperText.
 * Needed because Select does not have helperText.
 */
const FormHelperTextError = styled(FormHelperText).attrs({ error: true })`
    && {
        margin: 3px 14px 0;
    }
`;

/**
 * Makes button not full width
 */
const Button = styled(LoadingButton)`
    width: 130px;
`;
