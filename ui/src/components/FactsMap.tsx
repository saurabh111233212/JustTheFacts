import React, { useState, useEffect } from 'react';

import styled from 'styled-components';
import { Box, Typography, Grid, Avatar, Stack, Paper } from '@mui/material';
import Collapse from '@mui/material/Collapse';
import IconButton from '@mui/material/IconButton';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import Button from '@mui/material/Button';

import { useTheme } from '@mui/material/styles';

import { SOURCES, FACTS, CLUSTERS } from '../Stubs';

export interface SourceStruct {
    name: string;
    url: string;
    logo: string;
}

export interface FactStruct {
    fact: string;
    url: string;
    sourceName: string;
}

interface FactsMapProps {
    sources: SourceStruct[];
    clusters: FactStruct[][];
    setPivotArticle: (sourceIndex: number) => void;
    pivotIdx: number;
}

const FactsMap = ({sources, clusters, pivotIdx, setPivotArticle }: FactsMapProps) => {
    const [opens, setOpens] = useState<boolean[]>(new Array(clusters.length).fill(false));
    const [highlights, setHighlights] = useState<boolean[][]>([]);
    const theme = useTheme();
    // @ts-ignore
    const bgColor = theme.color2.T1;

    const toggleCluster = (idx: number) => {
        const newOpens = [...opens];
        newOpens[idx] = !newOpens[idx];
        setOpens(newOpens);
    }
    useEffect(() => {
        setHighlights(clusters.map(cluster => new Array(cluster.length).fill(false)));
    }, [clusters]);

    const toggleHighlight = (clusterIdx: number, factIdx: number) => {
        const newHighlights = [...highlights];
        const cluster = clusters[clusterIdx];
        const soureName = cluster[factIdx].sourceName;
        for (let i = 0; i < cluster.length; i++) {
            if (cluster[i].sourceName === soureName) {
                newHighlights[clusterIdx][i] = !newHighlights[clusterIdx][i];
            }
        }
        setHighlights(newHighlights);
    }

    const getHighlightFact = (clusterIdx: number) => {
        let factIdx = 0;
        if (highlights[clusterIdx]){
            const clusterHighlights = highlights[clusterIdx];
            const hlIndex = clusterHighlights.indexOf(true);
            if (hlIndex >= 0) {
                factIdx = hlIndex;
            }
        }
        return (<Typography variant="body1">{clusters[clusterIdx][factIdx].fact}</Typography>)
    }

    return (
        <div>
            <TableContainer component={Paper} sx={{padding: '4px 14px'}}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
                <TableRow>
                    <TableCell ></TableCell>
                    <TableCell ><Typography variant="body2">Fact</Typography></TableCell>
                    {sources.map((source, sourceIdx) => {
                        return (
                            <TableCell align="center">
                                <Button variant={pivotIdx == sourceIdx ? 'outlined': 'text'}>
                                <Typography variant="body2" onClick={() => { setPivotArticle(sourceIdx)}}>{source.name}</Typography>
                                </Button>
                            </TableCell>
                        )
                    })}
                </TableRow>
            </TableHead>
            <TableBody>
                {clusters.map((cluster, idx) => {
                    let fontColor = '#47515C';
                    let bgColor = 'white';
                    if (cluster.length >= 6) {
                        // @ts-ignore
                        bgColor = theme.color2.T4.hex;
                        fontColor = 'white';
                    } else if (cluster.length >= 5) {
                        // @ts-ignore
                        bgColor = theme.color2.T3.hex;
                    } else if (cluster.length >= 3) {
                        // @ts-ignore
                        bgColor = theme.color2.T2.hex;
                    } else if (cluster.length > 1){
                       // @ts-ignore
                       bgColor = theme.color2.T1.hex;
                    }
                    return (
                        <TableRow>
                            <TableCell scope="row" sx={{backgroundColor: bgColor, verticalAlign: 'top', borderBottom: '1px solid #AEB7C4'}}>
                                {cluster.length > 1 && (
                                    <IconButton
                                        aria-label="expand row"
                                        size="small"
                                        onClick={() => { toggleCluster(idx) }}>
                                        {opens[idx] ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                                    </IconButton>
                                )}
                            </TableCell>
                            <TableCell scope="row" sx={{backgroundColor: bgColor, borderBottom: '1px solid #AEB7C4', color: fontColor}} variant="body" size="small">
                                {opens[idx] ? (<>
                                    {cluster.map((fact, factIdx) => {
                                        const typoVariant = highlights[idx][factIdx] ? 'body2': 'body1';
                                        const textDecoration = highlights[idx][factIdx] ? 'underline': 'inherit';
                                        return (<Box sx={{padding: '5px 0'}}>
                                            <Typography variant={typoVariant} sx={{ textDecoration: textDecoration}}>{fact.fact}</Typography>
                                        </Box>)
                                    })}
                                    </>
                                ) : (
                                    <Box>
                                        {
                                            getHighlightFact(idx)
                                        }
                                    </Box>)
                                }
                            </TableCell>
                            {sources.map((source) => {
                                const hasSource = cluster.some((fact, factIdx) => fact.sourceName === source.name);
                                return (
                                    <TableCell align="center" sx={{borderBottom: '1px solid #AEB7C4', backgroundColor: bgColor, verticalAlign: 'top'}}>
                                        {hasSource && (
                                            <a href={source.url} target="_blank">
                                            <Avatar
                                                src={`/${source.logo}`}
                                                sx={{ width: 32, height: 32, borderBottom: '1px solid #AEB7C4', boxShadow: '0 1px 3px 0 rgba(0,0,0,.3)',
                                                margin: '0 auto'
                                            }}
                                                variant="rounded"
                                                imgProps={{style: {objectFit: 'contain', background: 'white'}}}
                                                onMouseOver={ () => { toggleHighlight(idx, cluster.findIndex((fact) => fact.sourceName === source.name))}}
                                                onMouseOut={ () => { toggleHighlight(idx, cluster.findIndex((fact) => fact.sourceName === source.name))}}
                                            >
                                                {source.name}
                                            </Avatar>
                                            </a>)}
                                    </TableCell>
                                )
                            })}
                        </TableRow>
                    )
                })}
            </TableBody>
      </Table>
    </TableContainer>
        </div>
    )
};

export default FactsMap;