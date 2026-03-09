FROM node:lts-bookworm
RUN apt update && apt install -y texlive-full pdf2svg fonts-inconsolata
COPY . /slides
WORKDIR /slides
RUN npm install && npm run compile_latex
CMD ["npm", "run", "start"]
