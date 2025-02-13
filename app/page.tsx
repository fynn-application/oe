'use client';

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, TextField, Button, Stack, Typography, Paper, List, CircularProgress, Box, AppBar, Toolbar } from '@mui/material';
import { styled } from '@mui/system';

interface HistoryItem {
  role: string;
  content: string;
}

const StyledPaper = styled(Paper)({
  padding: '1rem',
  marginTop: '1rem',
  marginBottom: '1rem',
  fontFamily: 'Open Sans, sans-serif',
});

const StyledButton = styled(Button)({
  height: '56px', // to match TextField height
});

const FixedAppBar = styled(AppBar)({
  position: 'fixed',
  top: 0,
  left: 0,
  right: 0,
  zIndex: 1100,
});


export default function Home() {
  const [question, setQuestion] = useState<string>('');
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [answer, setAnswer] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [adUrl, setAdUrl] = useState<string>('');
  const [adMessage, setAdMessage] = useState<string>('');

  const scrollToBottom = () => {
    window.scrollTo({
      top: document.documentElement.scrollHeight,
      behavior: 'smooth',
    });
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    const ad_response = await axios.post("http://localhost:8080/api/ad", { question, history })

    if (ad_response.data) {
      setAdUrl(ad_response.data.img_url)
      setAdMessage(ad_response.data.message)
    } else {
      setAdUrl('') // Could set a default ad as fallback here
      setAdMessage('')
    }

    console.log("Response", ad_response)
    setLoading(true);
    scrollToBottom();

    let start_time = new Date().getTime()
    try {
      const response = await axios.post('/api/ask', { question, history });
      setHistory([...history, { role: 'user', content: question }, { role: 'assistant', content: response.data.answer }]);
      setAnswer(response.data.answer);
      setQuestion('');
    } catch (error) {
      console.error('Error fetching the answer:', error);
    } finally {
      setLoading(false);
    }

    let end_time = new Date().getTime()
    if (ad_response.data) {
      axios.post("http://localhost:8080/api/record", { adId: ad_response.data.uid, durationViewed: (end_time - start_time) })
    }
  };

  const handleNewConversation = () => {
    setHistory([]);
    setAnswer('');
    setQuestion('');
    scrollToBottom();
  };

  useEffect(() => {
    if (!loading) {
      scrollToBottom();
    }
  }, [loading, history]);

  return (
    <>
      <FixedAppBar position="static">
        <Container maxWidth="md">
          <Toolbar disableGutters>
            <Typography variant="h6" style={{ flexGrow: 1, fontFamily: 'Roboto, sans-serif' }}>
              Simple Ask
            </Typography>
            <Button color="inherit" onClick={handleNewConversation}>New Conversation</Button>
          </Toolbar>
        </Container>
      </FixedAppBar>

      <Container maxWidth="md" style={{ marginTop: '120px', fontFamily: 'Roboto, sans-serif', marginBottom: '250px' }}>
        {history.length > 0 && (
          <List>
            {history.map((item, index) => (
              <StyledPaper elevation={3} key={index}>
                <Typography variant="body1" component="div">
                  <strong>{item.role.charAt(0).toUpperCase() + item.role.slice(1)}:</strong>
                </Typography>
                <Box component="div" dangerouslySetInnerHTML={{ __html: item.content.replace(/\n/g, '<br />') }} />
              </StyledPaper>
            ))}
          </List>
        )}
        <StyledPaper elevation={3}>
          <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <TextField
              label="Ask a question"
              variant="outlined"
              fullWidth
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              disabled={loading}  // Disable input while loading
            />
            <StyledButton type="submit" variant="contained" color="primary" disabled={loading}>
              Ask
            </StyledButton>
          </form>
        </StyledPaper>
        {loading && ((adUrl !== "" && (
          <Stack>
            <Box display="flex" justifyContent="center" alignItems="center" sx={{ mt: 1 }}>
              <img
                src={adUrl}
                loading="lazy"
                width="600pt"
              />
            </Box>
            <h2>
              {adMessage}
            </h2>

          </Stack >
        )) || (
            <Box display="flex" justifyContent="center" alignItems="center" mt={2}>
              <CircularProgress />
            </Box>
          ))
        }
      </Container >
    </>
  );
}
